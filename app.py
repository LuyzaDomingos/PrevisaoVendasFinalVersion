import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from fbprophet import Prophet
# Leitura de dados, por padrão em previsao/32.csv
data = pd.read_csv("previsao/32.csv", index_col=0)
data.fillna(value=0, inplace=True)
data.index = pd.to_datetime(data.index)
data = data.resample('W-THU').sum()
# Criação das novas séries temporais
data['j2_core'] = data['SMARTPHONE SAMSUNG GAL J2 CORE 16GB PRATA'] + data['SMARTPHONE SAMSUNG GAL J2 CORE 16GB PRETO']
data['j4_core'] = data['SMARTPHONE SAMSUNG GAL J4 CORE 16GB COBRE'] + data['SMARTPHONE SAMSUNG GAL J4 CORE 16GB PRETO']
data['j1_120'] = data['SMARTPHONE SAMSUNG GAL J1 J120 4G DB  DOURADO'] + data['SMARTPHONE SAMSUNG GAL J1 J120 4G DB  PRETO']
data['j6_32'] = data['SMARTPHONE SAMSUNG GAL J6 32GB PRATA'] + data['SMARTPHONE SAMSUNG GAL J6 32GB PRETO']
data['j1_100m'] = data['SMARTPHONE SAMSUNG GAL J1 J100M TIM BRANCO'] + data['SMARTPHONE SAMSUNG GAL J1 J100M TIM PRETO']
data['j2_prime'] = data['SMARTPHONE SAMSUNG GAL J2 PRIME 16GB TV DB PT'] + data['SMARTPHONE SAMSUNG GAL J2 PRIME 16GB TV DB RS'] + data['SMARTPHONE SAMSUNG GAL J2 PRIME 16GB TV DB DR']
data['j2_pro'] = data['SMARTPHONE SAMSUNG GAL J2 PRO J250M DB DR'] + data['SMARTPHONE SAMSUNG GAL J2 PRO J250M DB RS']
data['j2_prime_successor'] = data['j2_prime'] + data['SMARTPHONE SAMSUNG GAL J7 J700 DB BRANCO'] + data['SMARTPHONE SAMSUNG GAL J7 J700 DB DOURADO'] + data['SMARTPHONE SAMSUNG GAL J5 J500 DB BRANCO'] + data['SMARTPHONE SAMSUNG GAL J5 J500 DB DOURADO']
# Criação do dataframe de feriados
mothers = pd.DataFrame({
    'holiday': 'Dia das mães',
    'ds': ['2015-05-10', '2016-05-08', '2017-05-14', '2018-05-13', '2019-05-12'],
    'lower_window': -7,
    'upper_window': 0
})
fathers = pd.DataFrame({
    'holiday': 'Dia dos pais',
    'ds': ['2015-08-09', '2016-08-14', '2017-08-13', '2018-08-12', '2019-08-11'],
    'lower_window': -7,
    'upper_window': 0
})
valentines = pd.DataFrame({
    'holiday': 'Dia dos namorados',
    'ds': ['2015-06-12', '2016-06-12', '2017-06-12', '2018-06-12', '2018-06-12'],
    'lower_window': -7,
    'upper_window': 0
})
christmas = pd.DataFrame({
    'holiday': 'Natal',
    'ds': ['2015-12-25', '2016-12-25', '2017-12-25', '2018-12-25', '2019-12-25'],
    'lower_window': -8, # Incluindo a véspera
    'upper_window': 0
})
bf = pd.DataFrame({
    'holiday': 'Black friday',
    'ds': ['2015-11-27', '2016-11-25', '2017-11-24', '2018-11-25', '2019-11-24'],
    'lower_window': -7,
    'upper_window': 0
})
childrens = pd.DataFrame({
    'holiday': 'Dia das crianças',
    'ds': ['2015-10-12', '2016-10-12', '2017-10-12', '2018-10-12', '2019-10-12'],
    'lower_window': -7,
    'upper_window': 0
})
easter = pd.DataFrame({
    'holiday': 'Páscoa',
    'ds': ['2015-04-05', '2016-03-27', '2017-04-16', '2018-04-01', '2019-04-21'], # Domingo de páscoa
    'lower_window': -7,
    'upper_window': 0
})
new_year = pd.DataFrame({
    'holiday': 'Ano Novo',
    'ds': ['2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01'],
    'lower_window': -8, # Adicionar a véspera
    'upper_window': 0
})
carnival = pd.DataFrame({
    'holiday': 'Carnaval',
    'ds': ['2015-02-18', '2016-02-10', '2017-03-01', '2018-02-14', '2019-03-06'], # Quarta feira de cinzas
    'lower_window': -7, # Adicionar a véspera
    'upper_window': 0
})

holidays = pd.concat((mothers, fathers, valentines, christmas, bf, childrens, easter, new_year))

#data = pd.read_csv("previsao/dfw.csv")
forecast = pd.read_csv("previsao/forecast.csv")

forecast.index = pd.to_datetime(forecast['ds'])
forecast.drop(columns=['ds'], inplace=True)
              
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Avenir:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Previsão de vendas TESTE"

def getForecastFigure(filtered_data, product, split_date):
    # Criação do dataframe para o Prophet
    prophet_df = pd.DataFrame({'ds': filtered_data.index, 'y':filtered_data[product].values})
    size_train = len(data[:split_date])
    size_test = len(data[split_date:])
    
    prophet = Prophet(daily_seasonality=False, holidays=holidays)
    prophet.fit(prophet_df[:size_train])

    future = prophet.make_future_dataframe(periods=size_test, freq='W-THU')
    forecast = prophet.predict(future)
    forecast.index = pd.to_datetime(forecast['ds'])

    fig = px.line(range_x=['2015-01-01', '2019-06-09'],
                    range_y=[0, max(filtered_data[product] * 1.1)],
                    labels={'y': 'Quantidade Vendida', 'x': 'Período'},
                    title='Projeção de vendas')

    fig.add_trace(go.Scatter(x=data[size_train:].index, y=filtered_data[product][size_train:],
                        mode='markers',
                        name='Vendas observadas',
                        showlegend=False,
                        line={'color': '#045dd1'}))
       
    #fig.add_trace(go.Bar(x=data[split_date:].index, y=data[product][split_date:],
    #                    name='Vendas observadas',
    #                    showlegend=False))
                        
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

    return fig

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Previsão de vendas", className="header-title"
                ),
                html.P(
                    children="Visualização da série temporal de Smartphones"
                    " da família Samsung Galaxy J vendidos"
                    " entre 2015 e 2019",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": product, "value": product}
                                for product in data.columns
                            ],
                            value="j2_prime_successor",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Intervalo de datas",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.index.min().date(),
                            max_date_allowed=data.index.max().date(),
                            start_date=data.index.min().date(),
                            end_date=data.index.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales-chart-cumsum", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="sales-chart-period", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),

     

        html.Div(
            children=dcc.Graph(
                id="forecast-chart",
                config={"displayModeBar": False},
            ),
            className="wrapperSecond",
        ),
    ]
)

@app.callback(
# Lembrete: Se tiver mais de uma chamada de Output(...) colocar em uma lista as multiplas chamadas
    [Output("sales-chart-cumsum", "figure"), Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")],
    [
        Input("product-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

def update_charts(product, start_date, end_date):
    mask = (
        (data.index >= start_date)
        & (data.index <= end_date)
    )
    filtered_data = data.loc[mask, :]
    
    sales_cumsum_chart_figure = {
        "data": [
            {
                "x": filtered_data.index,
                "y": filtered_data[product].cumsum(),
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Quantidade vendida (acumulado)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#045dd1"],
        },
    }

    sales_period_chart_figure = {
        "data": [
            {
                "x": filtered_data.index,
                "y": filtered_data[product],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Quantidade vendida (semanal)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#045dd1"],
        },
    }
    
    forecast_chart_figure = getForecastFigure(filtered_data, product, '2018-01-01')
    
    return sales_cumsum_chart_figure, sales_period_chart_figure, forecast_chart_figure

    
if __name__ == "__main__":
    app.run_server(debug=True)
