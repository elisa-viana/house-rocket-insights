<h1 align="center"> House Rocket</h1>

<p align="center">Guia de negócios para compra e venda de imóveis</p>

<h1 align="center">
  <img alt="houserocketlogo" title="#houserocketlogo" src="./assets/House.png" />
</h1>

<h1 align="left"> 1. Introdução e o problema de negócio</h1>

<p align="justify">A House Rocket é uma empresa fictícia do ramo imobiliário que utiliza da tecnologia para tomar as melhores decisões em compra e revenda de propriedades. O objetivo desse projeto em Ciência de Dados foi encontrar as melhores oportunidades de negócio para maximizar o faturamento da empresa. <br />
<br />
A principal estratégia da empresa é comprar boas casas, em boas condições e com preços baixos, para depois revendê-las a preços mais elevados. A receita da empresa advém da diferença entre o valor de compra e de venda. <br />
<br />
Sabe-se que os imóveis possuem uma série de atributos que podem tornar a propriedade mais ou menos atrativas para potenciais compradores e vendedores. Atributos como a localização, vista, tamanho e período do ano podem afetar os preços.<br />
<br />
Esse projeto buscou responder as seguintes questões:</p>

  1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço? 
  2. Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço?

<h2 align="left"> 1.1. Conhecendo os dados</h2>

A base de dados utilizada refere-se a casas vendidas entre os anos de 2014 e 2015 em King's County, que inclui Seattle. Os dados estão disponíveis na plataforma [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction).

A tabela abaixo contém informações a respeito da base de dados. 

| Atributo | Significado |
| --- | --- |
|id| Identificação única de cada casa vendida|
|date| Data que cada casa foi vendida
|price| Valor de venda
|bedrooms| Número de quartos
|bathrooms| Número de banheiros, onde .5 refere-se a lavabos (i.e. sem chuveiro)
|sqft_living| Tamanho construído do imóvel em pés quadrados
|sqft_lot| Tamanho total do terreno em pés quadrados
|floors| Número de andares
|waterfront| Indica se a propriedade tem vista para a água ou não 
|view| Um índice de 0 a 4 para a qualidade da vista da propriedade, em que:  0 = sem vista, 1 = regular 2 = média, 3 = boa, 4 = excelente
|condition| Um índice de 1 a 5 para a integridade física da propriedade, em que: 1 = muito ruim, 2 = ruim, 3 = média, 4 = boa, 5= excelente
|grade| Um índice de 1 a 13 que classifica a qualidade da construção e do design do imóvel. 1-3: imóveis com baixa qualidade, 7: imóveis com qualidade média, 11-13: imóveis de alto padrão|
|sqft_above| O tamanho do sotão do imóvel em pés quadrados
|sqft_basement| O tamanho do porão do imóvel em pés quadrados
|yr_built| O ano em que a propriedade foi construída 
|yr_renovated| O ano em que o imóvel foi reformado pela última vez
|zipcode| O CEP do imóvel
|lat| Latitude
|long| Longitude
|sqft_living15| O tamanho do interior dos imóveis dos 15 vizinhos mais próximos (em pés quadrados)
|sqft_lot15| O tamanho do terreno dos imóveis dos 15 vizinhos mais próximos (em pés quadrados)


<h1 align="left"> 2. Premissas</h1>

<p align="justify"> Algumas premissas sobre os dados foram assumidas para a devida continuidade nas análises: </p>

- Data é referente ao dia que o imóvel foi disponibilizado para venda;
- Propriedades cujo ano de renovação for igual a 0 é considerado que não houve reforma;
- Através de análises exploratórias, assumi que a entrada única referente a um imóvel com 33 quartos significa, na verdade 3 quartos (a análise está disponível para consulta no arquivo kc_house_insights_project).

<h1 align="left"> 3. Planejamento da solução</h1>

<p align="justify"> O planejamento da solução consistiu em algumas sub-etapas: </p>

<h3 align="left"> 3.1. Entregáveis</h3>

- Tabela com as propriedades a serem adquiridas e o valor a serem vendidas;
- Aplicativo em nuvem com a apresentação geral dos dados, guia de negócios, insights gerados e principais conclusões. 

<h3 align="left"> 3.2. Ferramentas</h3>

- Python 3.9
- Pycharm
- Jupyter notebook
- Streamlit
- Streamlit cloud

<h3 align="left"> 3.3. Processo</h3>

Para responder as questões de negócio, os dados foram coletados, processados, transformados, limpos e explorados. 

- Questão de negócio 1: 
  - Para responder a primeira questão de negócio, os dados foram agrupados por zipcode e a mediana do preço dos grupos de imóveis foram obtidos. Primeiramente, foram consideradas como recomendadas para compra apenas imóveis cujo preço estava abaixo da mediana regional e que receberam classificação 3 ou acima de 3 para o atributo 'condition'; 
  - Como resultado, mais de 10 mil imóveis foram classificados como recomendados. Para melhorar o sistema de recomendação, uma nova filtragem dos dados foi realizada. Agora foram classificados como recomendados apenas imóveis cuja condição recebeu classificação 5, resultando em 698 imóveis; 
  - Utilizando os resultados obtidos pelos insights e seguindo o modelo de negócio da empresa, uma nova rodada de seleção foi estabelecida e os imóveis recomendados foram aqueles que: 
    1. Não possuiam vista para água; 
    2. Possuíam 3 banheiros ou menos; 
    3. Não foram reformados; 
    4. Possuem menos de 2 andares;
    5. A qualidade do design e construção é média ou baixa; 
    6. O índice de classificação da vista do imóvel é menor que 4. 

- Questão de negócio 2: 
  - 648 imóveis foram utilizados para responder a segunda questão. Os dados foram agrupados por zipcode e pela estação do ano em que os imóveis foram disponibilizados para venda. A mediana do preço de cada grupo foi obtida; 
  - Foi realizada uma comparação entre os preços dos imóveis e o valor mediano por estação e zipcode. Foi estabelecida uma margem de lucro da venda de 10% sobre os imóveis cujo preço estava acima do valor da mediana e de 30% sobre os imóveis cujo preço estava abaixo do valor da mediana; 
  - O lucro foi agrupado para cada estação do ano afim de entender qual o melhor período para vender os imóveis adquiridos. 

<h1 align="left"> 4. Principais insights</h1>

<p align="justify"> Conforme mencionado anteriormente, 648 imóveis com custo reduzido e boas condições foram recomendados para compra. A melhor estação do ano para revender as casas compradas é a primavera, quando a média do lucro por casa é mais elevada (cerca de US$84.000,00). Alguns atributos como: i) vista para água; ii) reforma; iii) número de andares; e iv) número de banheiros aumentam os preços dos imóveis em até 200%, aumentando o custo para a empresa e excluindo-os da lista de recomendações de compra.</p>

<h1 align="left"> 5. Resultado financeiro</h1>

<p align="justify"> Adotando a estratégia traçada através desse projeto, o lucro médio obtido por imóvel é de US$81.000,00, podendo chegar em um lucro líquido de até <strong>52 milhões<strong> de dólares.</p> 

<h1 align="left"> 6. Conclusão e próximos passos</h1>

<p align="justify"> O presente projeto em Ciência de Dados foi capaz de solucionar os problemas de negócio estabelecidos, entregando recomendações de boas oportunidades no ramo imobiliário levando em consideração o modelo de negócio da empresa. Apesar disso, o projeto pode ser refinado e melhorado posteriormente utilizados técnicas mais sofisticadas para resolver o problema de negócio. Dessa forma, os próximos passos podem consistir em: </p>

- Aprimorar a análise dos atributos que mais afetam os preços das casas (ex.: regressão múltipla) e, dessa forma, melhorar o sistema de recomendação; 
- Validar (ou não) as hipóteses estatisticamente (ex.: teste t, anova); 
- Fazer uma pesquisa de mercado para conhecer melhor os clientes e/ou potenciais clientes e suas demandas (ex.: quais os principais atributos que os clientes buscam ao comprar um imóvel?);
- Classificar os potenciais clientes e direcionar a compra e venda de imóveis de acordo com os diferentes perfis (ex.: direcionar a compra e venda de imóveis de baixo e alto padrão). 

<h1 align="left"> Outras informações</h1>

O aplicativo está disponível para consulta em: https://house-rocket-bg.streamlit.app/
