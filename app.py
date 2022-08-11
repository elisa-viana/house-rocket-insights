import pandas               as pd
import streamlit            as st
import plotly.express       as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout='wide')
# set title
st.title('Welcome to House Rocket Business Guide')
# set tabs
tab0, tab1, tab2, tab3 = st.tabs(['🏡 Home', '🔍 Data overview', '📝 Business guide', '📈 Insights'])

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data

def get_image(image_path):
    image = Image.open(image_path)
    return image

def initial_features (data):
    # correção da tipagem dos dados
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].dt.strftime("%Y-%m-%d")

    # remoção de variáveis não utilizadas na solução
    data = data.drop(columns=['sqft_above', 'sqft_living15', 'sqft_lot15'])

    # corrigindo outlier
    data.loc[data['bedrooms'] == 33, 'bedrooms'] = 3
    return data

def first_page (image):
    #first page
    with tab0:
        st.header('Project Summary')

        st.image(image, use_column_width='auto')

        st.write('''
        House Rocket is a digital company whose business model is purchasing and selling houses. 
        The aim of this project was to find the best opportunities in the real estate business to maximize the company's income. 
    
        The primary strategy is to buy great houses in good condition at low prices and sell those properties at higher prices. 
        However, the properties have a range of attributes that can make them more or less attractive to potential buyers and sellers. 
        Features such as location, water view, size, and time of the year can affect the prices. 
    
        The two main questions that this project sought to answer were:
    
        1. Which houses the House Rocket should buy and at what cost?  
        2. Once the house is in the company's possession, when is the best time to sell it and what would the sale price be? 
        ''')
        st.markdown("""---""")
        st.subheader('Main Results')
        st.write(
        "1. At first, only houses with good condition (index 3 or more) and with prices lower than the regional median were considered as recommended to buy. "
        "More than 10 thousend properties full filled the conditions.  \n"
        "2. To improve the recommendation system, only houses with excellent conditions were considered. "
        "We also use the information given by the insights to reduce the number of recommended properties.  \n"
        "3. The final list has 648 properties with good conditions and lower prices than the region median.  \n"
        "4. The best season to sell the properties is spring, when the average revenue per house is up to U$84,000.00.  \n"
        "5. The results of the insights sections are summarized in the table below.  \n"
        )

        #criando a tabela
        values = [['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10'],
                  ['Properties that has water view are 30% more expensive, on average.',
                   'Properties built before 1955 are 50% cheaper, on average.',
                   'Properties without basement have a total area 40% higher than properties that has basement, on average.',
                   'The Year-over-Year increase is 10%.',
                   'Properties with 3 bathrooms has a Month-over-Month increase of 15%.',
                   'Properties with 2 or more floors are 25% more expensive than the others, on average.',
                   'Renovated properties are 40% more expensive than non renovated properties, on average.',
                   'Properties that has 3 bathrooms or less are 30% cheaper than others, on average.',
                   'Properties with higher level of construction and design are, on average, 30% more expensive than others.',
                   'Properties with an excellent view are, on average, 40% more expensive than others.'],
                  ['True',
                   'False',
                   'False',
                   'False',
                   'False',
                   'True',
                   'True',
                   'True',
                   'True',
                   'True'],
                  ['Buy houses whithout water view.',
                   'Invest in properties regardless the year of construction.',
                   '-',
                   'Invest in properties regardeless of the year that the sell was announced.',
                   'Invest in properties in the lower cost months.',
                   'Invest in properties with 2 floors or less.',
                   'Invest in unrenovated properties and renovated them to sell.',
                   'Invest in properties with 3 bathrooms or less.',
                   'Invest in properties with a medium level of construction and design.',
                   'Invest in properties with a good to average view.']]

        table = go.Figure(data=[go.Table(
            columnorder=[1, 2, 3, 4],
            columnwidth=[80, 400, 80, 400],
            header=dict(
                values=[[''],
                        ['<b>Hypothesis</b>'],
                        ['<b>Result</b>'],
                        ['<b>Business action</b>']],
                line_color='darkslategray',
                fill_color=['gray', '#FFCBAA'],
                align=['center', 'center', 'center', 'center'],
                font=dict(color='black', size=16),
                height=40
            ),
            cells=dict(
                values=values,
                line_color='darkslategray',
                fill=dict(color=['gray', 'white']),
                align=['center', 'left', 'center', 'left'],
                font=dict(color=['white', 'black'], size=14),
                height=30)
        )
        ])
        table.update_layout(height=800)
        st.plotly_chart(table, use_container_width=True)
    return None

def business_questions (data):
    with tab1:
        # resolvendo primeira questão de negócio
        df_q1 = data.copy()

        # definindo o valor mediano por zipcode -> valor regional
        regional_price = df_q1[['price', 'zipcode']].groupby('zipcode').median().reset_index()
        regional_price.columns = ['zipcode', 'regional_price']

        # agregando os resultados na planilha
        df_q1_regional_price = pd.merge(df_q1, regional_price, how='inner', on='zipcode')

        # criando coluna que receberá o status do imóvel -> recomendado ou não recomendado
        for i in range(len(df_q1_regional_price)):
            if ((df_q1_regional_price.loc[i, 'price'] < df_q1_regional_price.loc[i, 'regional_price'])
                    & (df_q1_regional_price.loc[i, 'condition'] >= 3)):
                df_q1_regional_price.loc[i, 'Status'] = 'Recommended'

            else:
                df_q1_regional_price.loc[i, 'Status'] = 'Not recommended'

        # salvando tabela final
        df_q1_final = df_q1_regional_price.iloc[:, [0, 1, 2, 18, 13, 14, 15, 16, 17, 19]]
        df_q1_final.columns = ['id', 'date', 'price', 'regional price', 'year built', 'year of renovation', 'zipcode', 'lat', 'long', 'Status']

        # criando filtro
        st.sidebar.title('Filters')
        f_zipcode1 = st.sidebar.multiselect('Enter zipcode', df_q1_final['zipcode'].unique())

        # filtrando a 1a tabela
        # zipcode -> select rows
        if f_zipcode1 != []:
            df_q1_final = df_q1_final.loc[df_q1_final['zipcode'].isin(f_zipcode1), :]
        else:
            df_q1_final = df_q1_final.copy()

        # texto
        st.write('The data overview is displayed in this section. The table below shows the general information about '
                 'all the properties avaiable to buy. The "status" column provides the strategy for each property '
                 '(i.e. if the property is recommended or not to buy). More info about the strategy adopted for the recommendation system '
                 'are available in the "Home" section.')
        st.write('To see the properties information for each zipcode, please, choose one (or more) in the sidebar menu.')

        # mostrando os dados
        st.dataframe(df_q1_final, height=500)

    with tab2:
        # resolvendo segunda questão de negócio
        # filtrando os dados a partir dos insights
        df_q2 = df_q1_regional_price.loc[(df_q1_regional_price['Status'] == 'Recommended') &
                                         (df_q1_regional_price['condition'] == 5) &
                                         (df_q1_regional_price['waterfront'] == 0) &
                                         (df_q1_regional_price['bathrooms'] <= 3) &
                                         (df_q1_regional_price['yr_renovated'] == 0) &
                                         (df_q1_regional_price['floors'] < 2) &
                                         (df_q1_regional_price['grade'] < 11) &
                                         (df_q1_regional_price['view'] < 4)].copy()

        # corrigindo a data
        df_q2['date'] = pd.to_datetime(df_q2['date'])

        # criação de novos atributos
        df_q2['month'] = df_q2['date'].dt.month
        df_q2['season'] = df_q2['month'].apply(lambda x: "Summer" if (x >= 6) & (x <= 8) else
                                                         "Fall" if (x >= 9) & (x <= 11) else
                                                         "Winter" if (x == 1) | (x == 2) | (x == 12) else
                                                         "Spring")

        # obtendo a mediana do preço por zipcode e estação do ano
        seasonal_price = df_q2[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()
        seasonal_price.columns = ['zipcode', 'season', 'seasonal_price']

        # agregando os resultados na planilha
        df_q2_seasonal_price = pd.merge(df_q2, seasonal_price, how='inner', on=['zipcode', 'season'])

        # definindo as condições do preço de revenda
        for i in range(len(df_q2_seasonal_price)):
            if df_q2_seasonal_price.loc[i, 'price'] > df_q2_seasonal_price.loc[i, 'seasonal_price']:
                df_q2_seasonal_price.loc[i, 'selling_Price'] = df_q2_seasonal_price.loc[i, 'price'] * 1.1

            else:
                df_q2_seasonal_price.loc[i, 'selling_Price'] = df_q2_seasonal_price.loc[i, 'price'] * 1.3

        # calculando o lucro
        df_q2_seasonal_price['revenue'] = 'NA'
        for i in range(len(df_q2_seasonal_price)):
            df_q2_seasonal_price.loc[i, 'revenue'] = df_q2_seasonal_price.loc[i, 'selling_Price'] - \
                                                     df_q2_seasonal_price.loc[
                                                         i, 'price']

        # reorganizando e salvando a tabela final
        df_q2_seasonal_price = df_q2_seasonal_price.drop(columns=['month'])
        df_q2_seasonal_price = df_q2_seasonal_price.loc[:, ['id',
                                                            'date',
                                                            'yr_built',
                                                            'yr_renovated',
                                                            'zipcode',
                                                            'lat',
                                                            'long',
                                                            'Status',
                                                            'season',
                                                            'regional_price',
                                                            'seasonal_price',
                                                            'price',
                                                            'selling_Price',
                                                            'revenue']]

        df_q2_seasonal_price.columns = ['id', 'date', 'year built', 'year of renovation', 'zipcode', 'lat', 'long', 'Status', 'season', 'regional price',
                                        'price per season and region', 'price', 'selling price', 'revenue']

        # filtrando a 2a tabela
        # zipcode -> select rows
        if (f_zipcode1 != []):
            df_q2_seasonal_price = df_q2_seasonal_price.loc[df_q2_seasonal_price['zipcode'].isin(f_zipcode1), :]
        else:
            df_q2_seasonal_price = df_q2_seasonal_price.copy()

        # corrigindo o formato da data 2
        df_q2_seasonal_price['date'] = pd.to_datetime(df_q2_seasonal_price['date'])
        df_q2_seasonal_price['date'] = df_q2_seasonal_price['date'].dt.strftime("%Y-%m-%d")

        # texto
        st.write('In this section, only the recommended houses are displayed. More than 10 thousend properties were selected '
                 'with the previous recommendation strategy. To refine the recommendation we use the information given by the insights section. '
                 'The table below shows information about the suggested selling prices of each property selected and '
                 'their respective suggested selling price and revenue.')
        st.write('To see the properties information for each zipcode, please, choose one (or more) in the sidebar menu.')

        # mostrando os dados
        st.dataframe(df_q2_seasonal_price, height=500)

        c1, c2 = st.columns((1, 1))

        # fazendo o mapa
        with c1:
            st.header('Overview map')
            fig = px.scatter_mapbox(df_q2_seasonal_price,
                                lat="lat",
                                lon="long",
                                color="price",
                                size="price",
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                size_max=15,
                                zoom=10,
                                height=800,
                                mapbox_style="carto-positron",
                                hover_name='id',
                                hover_data=['selling price', 'revenue'])

            # texto
            st.write('The following map shows the properties recommended for buy. Bigger and darker spots represents more '
                     'expensives properties. We can notice that the properties close to a water resource are, in general, more expensives. '
                     'More details about the properties features and their relation with the price can be found in the "Insights" section.')

            # mostrando a figura
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.header('Price strategy')
            st.write('The image below shows the mean revenue by house sold for each season. '
                     'According to this, spring is the best season for sell the properties.')

            ps = px.histogram(data_frame=df_q2_seasonal_price, x='season', y='revenue',
                        labels={  # replaces default labels by column name
                            "revenue": "Revenue (U$)", 'season': ' '
                        }, histfunc='avg'
                        )
            st.plotly_chart(ps)
    return None

def insights (data):
    with tab3:
        col1, col2 = st.columns(2)

        #mudando o formato da data
        data['date'] = pd.to_datetime(data['date'])

        with col1:
            #hipótese 1
            st.subheader('H1')
            st.write('Properties that has water view are 30% more expensive, on average.')
            st.write('True. Waterfront properties are 212.64% more expensive than others.')

            df_h1 = data.copy()

            df_h1 = df_h1[['waterfront', 'price']].groupby('waterfront').mean().reset_index()
            df_h1['percentage'] = df_h1['price'].pct_change() * 100

            # plot
            h1 = px.bar(data_frame=df_h1, x='waterfront', y='price',
                        labels={  # replaces default labels by column name
                            "waterfront": "Water View", "price": "Price (U$)"
                        }
                        )
            h1.update_xaxes(type='category',
                            tickvals=[0, 1],
                            ticktext=['No', 'Yes']
                            )
            st.plotly_chart(h1, use_container_width=True)

            #hipótese 2
            st.subheader('H2')
            st.write('Properties built before 1955 are 50% cheaper, on average.')
            st.write('False. The price variation between properties built before and after 1955 is only 0.79%.')

            data['Ano_Construcao'] = data['yr_built'].apply(lambda x: "1930 - 1955" if x < 1955 else "1955 - 2015"
                                                                    )
            df_h2 = data[['Ano_Construcao', 'price']].groupby('Ano_Construcao').mean().reset_index()
            df_h2['pct'] = df_h2['price'].pct_change() * 100

            #plot
            h2 = px.bar(data_frame=df_h2, x='Ano_Construcao', y='price',
                        labels={  # replaces default labels by column name
                            "Ano_Construcao": "Construction Year", "price": "Price (U$)"
                        }
                        )

            st.plotly_chart(h2, use_container_width=True)

            #hipótese 3
            st.subheader('H3')
            st.write('Properties without basement have a total area 40% higher than properties that has basement, on average.')
            st.write('False. Basement-less properties has a total area only 22.56% higher than others, on average.')

            data['Porao'] = data['sqft_basement'].apply(lambda x: "Basement" if x > 0 else "No basement")
            df_h3 = data[['Porao', 'sqft_lot']].groupby('Porao').mean().reset_index()
            df_h3['pct'] = df_h3['sqft_lot'].pct_change() * 100

            # plot
            h3 = px.bar(data_frame=df_h3, x='Porao', y='sqft_lot',
                        labels={  # replaces default labels by column name
                            "Porao": "Basement", "sqft_lot": "Total property area (sqft)"
                        }
                        )

            st.plotly_chart(h3, use_container_width=True)

            #hipótese 4
            st.subheader('H4')
            st.write('The Year-over-Year increase is 10%.')
            st.write('False. The YoY increave corresponds only to 0.52%.')

            df_h4 = data.copy()

            #df_h4['date'] = pd.to_datetime(df_h4['date'])
            df_h4['Year'] = df_h4['date'].dt.strftime('%Y')
            df_h4 = df_h4[['Year', 'price']].groupby('Year').mean().reset_index()
            df_h4['pct'] = df_h4['price'].pct_change() * 100

            h4 = px.bar(data_frame=df_h4, x='Year', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)"
                        }
                        )

            st.plotly_chart(h4, use_container_width=True)

            #hipótese 5
            st.subheader('H5')
            st.write('Properties with 3 bathrooms has a Month-over-Month increase of 15%.')
            st.write('False. The MoM variation has no pattern.')

            df_h5 = data.loc[data['bathrooms'] == 3].copy()

            df_h5['mês'] = df_h5['date'].dt.strftime('%Y-%m')
            df_h5['Year'] = df_h5['date'].dt.strftime('%Y')

            df_h5 = df_h5[['mês', 'price']].groupby('mês').mean().reset_index()
            df_h5['pct'] = df_h5['price'].pct_change() * 100
            df_h5['pct_variacao'] = df_h5['pct'].apply(lambda x: 'Positiva' if x > 0 else 'Negativa')

            h5 = px.bar(data_frame=df_h5, x='mês', y='pct', color="pct_variacao", barmode="group",
                        labels={"pct": "Price variation (%)", "mês": " "},
                        color_discrete_map={
                            'Negativa': '#EF553B',
                            'Positiva': '#636EFA'
                        }
                        )
            h5.update_yaxes(ticksuffix="%")
            h5.update_layout(showlegend=False)

            st.plotly_chart(h5, use_container_width=True)

        with col2:
            #hipótese 6
            st.subheader('H6')
            st.write('Properties with 2 or more floors are 25% more expensive than the others, on average.')
            st.write('True. Properties with 2 or more floors are 29.46% more expensive than the others.')

            df_h6 = data.copy()

            df_h6['price_floors'] = df_h6['floors'].apply(lambda x: "2 or more" if x >= 2 else "Less than 2")
            df_h6 = df_h6[['price_floors', 'price']].groupby('price_floors').mean().reset_index()
            df_h6['pct'] = df_h6['price'].pct_change() * 100

            #plot
            h6 = px.bar(data_frame=df_h6, x='price_floors', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)", "price_floors": "Number of floors"
                        }
                        )

            st.plotly_chart(h6, use_container_width=True)

            #hipótese 7
            st.subheader('H7')
            st.write('Renovated properties are 40% more expensive than non renovated properties, on average.')
            st.write('True. Renovated properties are 43.37% more expensive than others.')

            df_h7 = data.copy()

            df_h7['renovation'] = df_h7['yr_renovated'].apply(lambda x: 'Renovated' if x > 0 else 'Not renovated')
            df_h7 = df_h7[['renovation', 'price']].groupby('renovation').mean().reset_index()
            df_h7['pct'] = df_h7['price'].pct_change() * 100

            #plot
            h7 = px.bar(data_frame=df_h7, x='renovation', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)", "renovation": " "
                        }
                        )

            st.plotly_chart(h7, use_container_width=True)

            # hipótese 8
            st.subheader('H8')
            st.write('Properties that has 3 bathrooms or less are 30% cheaper than others, on average.')
            st.write('')
            st.write('True. Properties that has 3 bathrooms or less are 124.68% cheaper than others.')

            df_h8 = data.copy()

            df_h8['p_bathrooms'] = df_h8['bathrooms'].apply(lambda x: '3 or less' if x <= 3 else 'More than 3')
            df_h8 = df_h8[['p_bathrooms', 'price']].groupby('p_bathrooms').mean().reset_index()
            df_h8['pct'] = df_h8['price'].pct_change() * 100

            #plot
            h8 = px.bar(data_frame=df_h8, x='p_bathrooms', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)", "p_bathrooms": "Number of bathrooms"
                        }
                        )

            st.plotly_chart(h8, use_container_width=True)

            # hipótese 9
            st.subheader('H9')
            st.write('Properties with higher level of construction and design are, on average, 30% more expensive than others.')
            st.write('True. A higher level of construction and design increase the properties price in 227.21% on average.')

            df_h9 = data.copy()

            df_h9['design_level'] = df_h9['grade'].apply(lambda x: 'High' if x > 10 else
            'Average or low')

            df_h9 = df_h9[['design_level', 'price']].groupby('design_level').mean().reset_index()
            df_h9['pct'] = df_h9['price'].pct_change() * 100

            #plot
            h9 = px.bar(data_frame=df_h9, x='design_level', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)", "design_level": "Level of design and construction"
                        }
                        )

            st.plotly_chart(h9, use_container_width=True)

            # hipótese 10
            st.subheader('H10')
            st.write('Properties with an excellent view are, on average, 40% more expensive than others.')
            st.write('True. A better view is responsible for a 64.05% increase in house prices, on average.')

            df_h10 = data.copy()

            df_h10['e_view'] = df_h10['view'].apply(lambda x: 'Excellent' if x == 4 else 'Good to low')

            df_h10 = df_h10[['e_view', 'price']].groupby('e_view').mean().reset_index()
            df_h10['pct'] = df_h10['price'].pct_change() * 100

            #plot
            h10 = px.bar(data_frame=df_h10, x='e_view', y='price',
                        labels={  # replaces default labels by column name
                            "price": "Price (U$)", "e_view": "View quality"
                        }
                        )

            st.plotly_chart(h10, use_container_width=True)
    return None


if __name__ == '__main__':
    #data extraction
    path = 'kc_house_data.csv'
    data = get_data(path)

    image_path = 'House.png'
    image = get_image(image_path)

    #pages construction
    data = initial_features(data)
    first_page(image)
    business_questions(data)
    insights(data)








