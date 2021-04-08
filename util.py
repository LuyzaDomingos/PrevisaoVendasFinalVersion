import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from fbprophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from random import randint

import dash_core_components as dcc
import dash_html_components as html

from app import app

# Criação do dataframe de feriados
mothers = pd.DataFrame({
    'holiday': 'Dia das mães',
    'ds': ['2015-05-10', '2016-05-08', '2017-05-14', '2018-05-13', '2019-05-12', '2020-05-10', '2021-05-09'],
    'lower_window': 0,
    'upper_window': 0
})
fathers = pd.DataFrame({
    'holiday': 'Dia dos pais',
    'ds': ['2015-08-09', '2016-08-14', '2017-08-13', '2018-08-12', '2019-08-11', '2020-08-09', '2021-06-20'],
    'lower_window': 0,
    'upper_window': 0
})
valentines = pd.DataFrame({
    'holiday': 'Dia dos namorados',
    'ds': ['2015-06-12', '2016-06-12', '2017-06-12', '2018-06-12', '2019-06-12', '2020-06-12', '2021-06-12'],
    'lower_window': 0,
    'upper_window': 0
})
christmas = pd.DataFrame({
    'holiday': 'Natal',
    'ds': ['2015-12-25', '2016-12-25', '2017-12-25', '2018-12-25', '2019-12-25', '2020-12-25', '2020-12-25'],
    'lower_window': -1, # Incluindo a véspera
    'upper_window': 0
})
bf = pd.DataFrame({
    'holiday': 'Black friday',
    'ds': ['2015-11-27', '2016-11-25', '2017-11-24', '2018-11-25', '2019-11-24', '2020-11-27', '2021-11-25'],
    'lower_window': 0,
    'upper_window': 0
})
childrens = pd.DataFrame({
    'holiday': 'Dia das crianças',
    'ds': ['2015-10-12', '2016-10-12', '2017-10-12', '2018-10-12', '2019-10-12', '2020-10-12', '2021-10-12'],
    'lower_window': 0,
    'upper_window': 0
})
easter = pd.DataFrame({
    'holiday': 'Páscoa',
    'ds': ['2015-04-05', '2016-03-27', '2017-04-16', '2018-04-01', '2019-04-21', '2020-04-12', '2021-04-04'], # Domingo de páscoa
    'lower_window': -2, # Incluindo o fim de semana
    'upper_window': 0
})
new_year = pd.DataFrame({
    'holiday': 'Ano Novo',
    'ds': ['2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01'],
    'lower_window': -1, # Adicionar a véspera
    'upper_window': 0
})
carnival = pd.DataFrame({
    'holiday': 'Carnaval',
    'ds': ['2015-02-18', '2016-02-10', '2017-03-01', '2018-02-14', '2019-03-06', '2020-02-26', '2021-02-17'], # Quarta feira de cinzas
    'lower_window': -4, # Incluindo sábado, domingo, segunda e terça
    'upper_window': 0
})

holidays = pd.concat((mothers, fathers, valentines, christmas, bf, childrens, easter, new_year))

def heroku():
    return True

def get_forecast_figure(filtered_data, product, split_date, freq='D'):
    size_train = len(filtered_data[:split_date])
    size_test = len(filtered_data[split_date:])
    path = "previsao/forecasts/" + freq + "/" + product.replace(" ", "_").replace("/", "_") + ".csv"
    # Uma espécie de cache para não repetir a computação do modelo toda vez que selecionar um produto
    try:
        forecast = pd.read_csv(path)
        forecast.index = pd.to_datetime(forecast['ds'])
    except:
        # Criação do dataframe para o Prophet
        prophet_df = pd.DataFrame({'ds': filtered_data.index, 'y':filtered_data[product].values})
        
        prophet = Prophet(daily_seasonality=False, holidays=holidays)
        prophet.fit(prophet_df[:size_train])

        future = prophet.make_future_dataframe(periods=size_test, freq=freq)
        forecast = prophet.predict(future)
        forecast.index = pd.to_datetime(forecast['ds'])
        if heroku() is False:
            forecast.to_csv(path)

    forecast['yhat'] = forecast['yhat'].apply(lambda x : 0 if x < 0 else round(x))
    forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x : 0 if x < 0 else round(x))
    forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x : 0 if x < 0 else round(x))

    fig = px.line(range_x=['2018-01-01', '2021-03-12'],
                    range_y=[0, max(filtered_data[product] * 1.1)],
                    labels={'y': 'Quantidade Vendida', 'x': 'Período'},
                    title='Projeção de vendas')

    fig.add_trace(go.Scatter(x=filtered_data[size_train:].index, y=filtered_data[product][size_train:],
                        mode='markers',
                        name='Vendas observadas',
                        showlegend=False,
                        line={'color': '#045dd1'}))

    fig.add_trace(go.Scatter(x=filtered_data[:size_train].index, y=filtered_data[product][:size_train],
                        mode='lines',
                        name='Vendas observadas',
                        line={'color': '#045dd1'}))
                        
    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat'][size_train:],
                        mode='lines',
                        name='Vendas projetadas',
                        line={'color': '#d10b04'}))

    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat_lower'][size_train:],
                        #mode='none',
                        name='Limite inferior',
                        showlegend=False,
                        line_color='rgba(192, 43, 29, 0.2)'))
                        
    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat_upper'][size_train:],
                        #mode='none',
                        fill='tonexty',
                        fillcolor='rgba(192, 43, 29, 0.2)',
                        name='Limite superior',
                        showlegend=False,
                        line_color='rgba(192, 43, 29, 0.2)'))
                        
    fig.add_shape(type='line',
                  x0=split_date,
                  y0=0,
                  x1=split_date,
                  y1=999,
                  line={'color': '#c4c7cc'})
                  
    fig.layout.xaxis.linecolor='rgba(0, 0, 0, 1)'
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'

    return fig, forecast
    
def get_sales_figure(filtered_data, product):
    # Criar uma figura com eixos secundários
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(title_text="Vendas observadas", xaxis_range=['2018-01-01', '2021-03-12'])
    
    # Adicionar as linhas
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product].cumsum(), name="Vendas acumuladas", line={'color': '#045dd1'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product], name="Vendas no período", line={'color': 'rgba(101, 156, 0, 0.8)'}), secondary_y=True)

    # Nome dos eixos
    fig.update_yaxes(title_text="Vendas acumuladas", secondary_y=False)
    fig.update_yaxes(title_text="Vendas no período", secondary_y=True)

    # Linha y = 0
    fig.add_shape(type='line', x0='2018-01-01', y0=0, x1='2021-03-12', y1=0, line={'color': 'rgba(0, 0, 0, 1)'})
    # Cores do gráfico
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'
    
    return fig

def get_indicators_figure(filtered_data, forecast, product, split_date):
    size_train = len(filtered_data[:split_date])
    size_test = len(filtered_data[split_date:])

    mse = mean_squared_error(filtered_data[product][size_train:], forecast['yhat'][size_train:len(filtered_data)])
    mad = mean_absolute_error(filtered_data[product][size_train:], forecast['yhat'][size_train:len(filtered_data)])

    fig = go.Figure()
    fig.update_layout(height=120, margin=dict(l=40, r=40, t=40, b=8))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = mse,
        title = {"text": "Erro médio quadrático"},
        #delta = {'reference': 400, 'relative': True},
        domain = {'row': 0, 'column': 0}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = mad,
        #title = {"text": "Erro médio absoluto<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
        title = {'text': 'Erro médio absoluto'},
        #delta = {'reference': 400, 'relative': True},
        domain = {'row': 0, 'column': 1}))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Speed"},
            'mode' : "number+delta+gauge",
            'delta' : {'reference': 90}}]
                             }})

    return fig

def get_list(base_dict):
    child = []

    fig = go.Figure()
    fig.update_layout(height=80, margin=dict(l=40, r=40, t=40, b=8), plot_bgcolor='rgb(255,0,0)')

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = randint(0, 999),
        title = {"text": "Vendas Previstas"},
        delta = {'reference': randint(0, 999), 'relative': True, 'position': 'right'},
        domain = {'row': 0, 'column': 0}))

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = randint(0, 99),
        title = {"text": "Estoque atual"},
        delta = {'reference': randint(0, 99), 'relative': True, 'position': 'right'},
        domain = {'row': 0, 'column': 1}))

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = randint(0, 9999999),
        title = {"text": "Valor das vendas"},
        number = {'prefix': "R$"},
        delta = {'reference': randint(0, 9999999), 'relative': True, 'position': 'right'},
        domain = {'row': 0, 'column': 2}))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Speed"},
            'mode' : "number+delta+gauge",
            'delta' : {'reference': 90}}]
                             }})
    child.append(html.Div(children=[dcc.Graph(id="sales-chart-period-header", config={"displayModeBar": False}, figure=fig)], className="card small-margin"))

    for item in base_dict:
        fig = go.Figure()
        fig.update_layout(height=80, margin=dict(l=40, r=40, t=8, b=8), plot_bgcolor='#333333')

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 999),
            title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
            delta = {'reference': randint(0, 999), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 99),
            title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
            delta = {'reference': randint(0, 99), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 1}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 9999999),
            title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
            number = {'prefix': "R$"},
            delta = {'reference': randint(0, 9999999), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 2}))

        fig.update_layout(
            grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
            template = {'data' : {'indicator': [{
                'title': {'text': "Speed"},
                'mode' : "number+delta+gauge",
                'delta' : {'reference': 90}}]
                                 }})
        child.append(html.Div(children=[html.Div(children=[html.Img(src=app.get_asset_url('categorias/' + item + '.png')), dcc.Link(item, href='index', className='link white-bg')], className='class-header'), dcc.Graph(id="sales-chart-period-" + item, config={"displayModeBar": False}, figure=fig)], className="card small-margin"))

    return child