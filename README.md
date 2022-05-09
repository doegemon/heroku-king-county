# heroku-king-county
Projeto de análise de dados deployado no Heroku com mapa, dataframes e gráficos sobre os imóveis disponíveis para venda em King County, Washington, EUA. 

# 1.0 Contexto
Inicialmente, quero destacar que esse é meu primeiro projeto de Análise de Dados, onde tentei aprender o máximo sobre ETL (Extract, Transform and Load), visualização e manipulação de dados, visando responder algumas perguntas fictícias de negócios, bem como testar algumas hipóteses.

## 1.1 Perguntas de Negócio
 a) Quais imóveis disponíveis para comprar estão com um 'bom preço'?
 
 b) Uma vez efetuada a compra de um imóvel, qual o melhor momento para vendê-lo? Por qual preço?
 
## 1.2 Hipóteses de Negócio
 a) Imóveis que posseum vista para a água são 30% mais caros
 
 b) Imóveis com data de construção anterior a 1955 são 50% mais baratos
 
 c) Imóveis sem porão possuem área total 40% maior que os imóveis sem porão
 
 d) O crescimento dos preços dos imóveis YoY (Year over Year) é de 10%
 
 e) Entre as casas construída antes de 1955, as renovadas tem um preço 10% maior
 
# 2.0 Premissas
Para responder a segunda pergunta de negócio, especificamente sobre o melhor momento para vender um imóvel, fiz uma análise com base nas estações do ano, sendo que considerei Verão e Primavera como 'Summer' e Inverno e Outono como 'Winter'. 

# 3.0 Soluções

## 3.1 Respostas
 a) A recomendação de comprar de determinado imóvel foi feita com base na comparação entre seu preço e a mediana do preço dos imóveis na região em que ele se encontra (baseado no 'zipcode', ou código postal). Ainda, levei em conta a condição do imóvel ('condition'), tendo como base o valor 3 (o valor varia de 1 a 5).
 
 Dos 21.436 imóveis constantes do dataset, temos 10.499 imóveis com a recomendação de comprar, levando em consideração esse filtro. 
 
 b) Primeiro foi feita uma análise para verificar se as estações do ano afetam o preço dos imóveis, sendo que pode-se concluir que no verão o valor dos imóveis tende a ser maior que a mediana do preço dos imóveis na região em que ele se encontra, enquanto no inverno ocorre o oposto.
 
 Depois, com base nos imóveis que foram anunciandos durante o verão e que estavam com o preço acima da mediana do preço dos imóveis da região, foi verificado que, na medianda, os imóveis estavam sendo anunciados com um preço 24.5% maior que os imóveis da região. 
 
 Assim, com base nos imóveis com recomendação de compra, foi sugerido um possível preço de venda mediante a aplicação desse adicional de 24.5%, calculando o possível lucro em cada operação.

## 3.2 Hipóteses
 a) FALSA, na mediana os imóveis com vista para água são 300% mais caros que imóveis sem vista para água.
 
 b) FALSA, na mediana não há diferença de preço entre imóveis construídos antes e depois de 1955.
 
 c) FALSA, na mediana os imóveis sem porão possuem uma área total só 2% maior que imóveis sem porão. 
 
 d) FALSA, na mediana a evolução dos preços de 2014 para 2015 (YoY) foi de somente 0.5%.
 
 e) VERDADEIRA, entre os imóveis construídos antes de 1955 os que foram renovados tem um preço 35% maior em comparação aos imóveis não renovados. 
 
# 4.0 Conclusões
Esse foi um projeto visando trazer alguns Insights sobre os imóveis disponíveis para compra em King County, Washington, EUA.

As respostas para as perguntas de negócio são apenas sugestões com base na análise de dados, mas que servem de fundamento para a realização de negócios que podem trazer bons resultados, sendo demonstrado os imóveis com 'bom preço' e sugerido um possível preço de venda levando em conta a estação do ano.

De igual forma, as hipóteses aqui testadas também trazem informações importantes para a tomada de decisões e forma de condução de negócios, principalmente a última, onde se demonstrou que os imóveis antigos renovados tem um valor maior em comparação aos imóveis antigo não renovados. 

# Referências

### Dataset 
https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
