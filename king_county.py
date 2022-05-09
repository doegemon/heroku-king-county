import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px

pd.set_option('display.float_format', lambda x: '%.2f' % x)

st.set_page_config(layout='centered')


# Functions
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data


def format_data(data):
    # Convertendo de 'object' para 'date'
    data['date'] = pd.to_datetime(data['date'])
    # Removendo 'id's duplicados
    data.drop_duplicates(subset='id', keep='first', inplace=True)
    # Deletando colunas que não irão ser utilizadas
    data = data.drop(['sqft_living15', 'sqft_lot15'], axis=1)
    return data


def transform_data(data):
    st.title('Análise da Venda de Imóveis em King County, EUA')
    st.markdown('O intuito de analisar este dataset foi procurar responder algumas perguntas de negócio a respeito dos'
                ' imóveis anunciados na região.')
    st.image('kingcounty.jpg')
    # Criando coluna para descobrir o preço mediano por região
    median_price = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    df = pd.merge(data, median_price, on='zipcode', how='inner')
    df.rename(columns={'price_x': 'price', 'price_y': 'median_price'}, inplace=True)
    for i in range(len(df)):
        if (df.loc[i, 'price'] < df.loc[i, 'median_price']) & (df.loc[i, 'condition'] >= 3):
            df.loc[i, 'recommendation'] = 'Comprar'
        else:
            df.loc[i, 'recommendation'] = "Não Comprar"

    # Atribuindo uma estação baseada na 'date'
    for i in range(len(df)):
        if (df.loc[i, 'date'] >= pd.to_datetime('2014-05-02', format='%Y-%m-%d')) and (
                df.loc[i, 'date'] <= pd.to_datetime('2014-09-22', format='%Y-%m-%d')):
            df.loc[i, 'season'] = 'summer'
        elif (df.loc[i, 'date'] >= pd.to_datetime('2014-09-23', format='%Y-%m-%d')) and (
                df.loc[i, 'date'] <= pd.to_datetime('2015-03-19', format='%Y-%m-%d')):
            df.loc[i, 'season'] = 'winter'
        else:
            df.loc[i, 'season'] = 'summer'

    # Criando coluna para indicar se o preço está acima do preço mediano da região
    for i in range(len(df)):
        if df.loc[i, 'price'] > df.loc[i, 'median_price']:
            df.loc[i, 'is_higher'] = 'yes'
        else:
            df.loc[i, 'is_higher'] = 'no'

    # Quão acima os preços estão acima do preço mediano da região? (Em %)
    for i in range(len(df)):
        if (df.loc[i, 'season'] == 'summer') & (df.loc[i, 'price'] > df.loc[i, 'median_price']):
            df.loc[i, 'difference'] = (df.loc[i, 'price'] * 100) / df.loc[i, 'median_price'] - 100
        else:
            df.loc[i, 'difference'] = 'NA'

    # Adicionando a percentagem mediana como recomendação de preço de venda e calculando o lucro
    for i in range(len(df)):
        if df.loc[i, 'recommendation'] == 'Comprar':
            df.loc[i, 'sell_price'] = df.loc[i, 'price'] + (df.loc[i, 'price'] * 24.5 / 100)
        else:
            df.loc[i, 'sell_price'] = 'NA'
    for i in range(len(df)):
        if df.loc[i, 'recommendation'] == 'Comprar':
            df.loc[i, 'profit'] = df.loc[i, 'sell_price'] - df.loc[i, 'price']
        else:
            df.loc[i, 'profit'] = 'NA'

    # Criando colunas para testar hipóteses
    df['is_waterfront'] = df['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')
    df['is_old'] = df['yr_built'].apply(lambda x: 'yes' if x <= 1955 else 'no')
    df['basement'] = df['sqft_basement'].apply(lambda x: 'no' if x == 0 else 'yes')
    df['yoy'] = df['date'].apply(lambda x: 2014 if x <= pd.to_datetime('2014-12-31', format='%Y-%m-%d') else 2015)
    df['renovated'] = df['yr_renovated'].apply(lambda x: 'yes' if x > 0 else 'no')

    return df


def buy_houses(data):
    st.header('Recomendações de Compra:')
    # Imóveis para comprar
    buy_table = data[['id', 'price', 'zipcode', 'median_price', 'condition', 'recommendation']]
    st.dataframe(buy_table.style.format(subset=['price', 'median_price'], formatter='{:.2f}'))
    buy_total = len(data.loc[data['recommendation'] == 'Comprar', 'id'])
    st.markdown(f'No total, temos {buy_total} imóveis com a recomendação de Comprar, tendo como fundamento eles estarem'
                f' sendo anunciados por um preço abaixo do preço mediano da região.')
    st.header('Mapa de Recomendações')
    f_buy = st.checkbox('Apenas Imóveis com Recomendação de Compra')
    if f_buy:
        data = data[data['recommendation'] == 'Comprar']
    else:
        data = data.copy()
    rec_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to(rec_map)
    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']], popup=f'Preço: {row["price"]} Recomendação: {row["recommendation"]}')\
            .add_to(marker_cluster)
    folium_static(rec_map)
    return None


def sell_houses(data):
    st.header('Recomendação de Venda')
    # Qual estação os preços anunciados estão acima do preço mediano da região?
    data_season = data[['id', 'is_higher', 'season']].groupby(['is_higher', 'season']).count().reset_index()
    st.dataframe(data_season)
    st.markdown('A coluna "is_higher" indica se o preço do imóvel foi anunciado ou não acima do preço mediano da '
                'região. '
                'Portanto, pode-se concluir que no verão o valor dos imóveis tende a ser maior que o preço '
                'mediano da região.')
    # Imóveis para vender
    sell_table = data[data['sell_price'] != 'NA']
    sell_table = sell_table[['id', 'zipcode', 'median_price', 'price', 'sell_price', 'profit']]
    st.dataframe(sell_table.style.format(subset=['median_price', 'price', 'sell_price', 'profit'], formatter='{:.2f}'))
    st.markdown('''Tendo como base os imóveis com recomendação de "Comprar", podemos aplicar uma margem de lucro e 
    sugerir como preço de venda, demonstrando o lucro de cada operação''')
    return None


def data_hypothesis(data):
    st.header('Testando Hipóteses')
    # Testando hipóteses
    st.subheader('1. Imóveis com vista para a água são 30% mais caros, na mediana')
    data_water = data[['is_waterfront', 'price']].groupby('is_waterfront').median().reset_index()
    fig_water = px.bar(data_water, x='is_waterfront', y='price', text_auto=True)
    st.plotly_chart(fig_water)
    st.markdown('Na mediana, os imóveis com vista para água são 300% por mais caros')

    st.subheader('2. Imóveis com data de construção menor que 1955 são 50% mais baratos, na mediana')
    data_old = data[['is_old', 'price']].groupby('is_old').median().reset_index()
    fig_old = px.bar(data_old, x='is_old', y='price', text_auto=True)
    st.plotly_chart(fig_old)
    st.markdown('Considerando "yes" como o grupo de imóveis construídos antes de 1955, na mediana não há diferença '
                'de preços.')

    st.subheader('3. Imóveis sem porão possuem área total 40% maior que imóveis com porão, na mediana')
    data_basement = data[['basement', 'sqft_lot']].groupby('basement').median().reset_index()
    fig_basement = px.bar(data_basement, x='basement', y='sqft_lot', text_auto=True)
    st.plotly_chart(fig_basement)
    st.markdown('Imóveis sem porão possuem uma área total 2% maior que imóveis com porão.')

    st.subheader('4. Crescimento do preço dos imóveis YoY é de 10%, na mediana')
    data_yoy = data[['yoy', 'price']].groupby('yoy').median().reset_index()
    fig_yoy = px.bar(data_yoy, x='yoy', y='price', text_auto=True)
    st.plotly_chart(fig_yoy)
    st.markdown('A evolução dos preços de 2014 para 2015 foi de 0,5% tão somente.')

    st.subheader('5. Entre casas construídas antes de 1955, as renovadas tem um preço 10% maior')
    data_renew = data[['is_old', 'renovated', 'price']].groupby(['is_old', 'renovated']).median().reset_index()
    fig_renew = px.histogram(data_renew, x='is_old', y='price', color='renovated', barmode='group', height=400,
                             text_auto=True)
    st.plotly_chart(fig_renew)
    st.markdown('Considerando "yes" como o grupo de imóveis construídos antes de 1955, percebe-se que as casas '
                'renovadas tem um preço 35% maior.')
    return None


if __name__ == '__main__':
    # ETL
    # Extraction
    path = 'kc_house_data.csv'
    data = get_data(path)

    # Transformation
    data = format_data(data)
    data = transform_data(data)
    buy_houses(data)
    sell_houses(data)
    data_hypothesis(data)
