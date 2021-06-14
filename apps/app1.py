# Aplicativo 1 (Previsão por produtos)
import json
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
# Dependências do Dash
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash import no_update
# API de previsão de séries temporais
from fbprophet import Prophet
# Funções de plotagem
from util import get_forecast_figure, get_sales_figure, get_indicators_figure, heroku

from app import app

# Leitura dos dados, amostragem diária
data_d = pd.read_csv("previsao/geral.csv", index_col=0)
data_d.fillna(value=0, inplace=True)
data_d.index = pd.to_datetime(data_d.index)
data_d = data_d[:'2021-03-12']
# Amostragem semanal
data_w = data_d.resample('W-MON').sum()
# Amostragem mensal
data_m = data_d.resample('M').sum()
# Dicionário de categorias
categories_dict = json.load(open('previsao/subcategorias.json'))
# Dicionário de frequências
freq_dict = {
    'Diário': 'D',
    'Semanal': 'W-MON',
    'Mensal': 'M'
}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Avenir:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
    
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Previsão por Produtos", className="header-title"),
                html.P(children="Visualização e previsão de séries temporais referentes à vendas de produtos", className="header-description"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
                #html.Button("Baixe a previsão (.csv)", id="bt-download", className="bt"),
                #Download(id="download"),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Categoria", className="menu-title"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[{"label": key, "value": key} for key in list(categories_dict.keys())],
                            value="ELETRO INFORMATICA",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": product, "value": product}
                                for product in categories_dict["ELETRO INFORMATICA"]
                            ],
                            value="TABLET NB316 M7S 16GB QUAD CORE PRETO",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Frequência", className="menu-title"),
                        dcc.Dropdown(
                            id="frequency-selector",
                            options=[{"label": key, "value": value} for key, value in freq_dict.items()],
                            value="D",
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
                            min_date_allowed=data_d.index.min().date(),
                            max_date_allowed=data_d.index.max().date(),
                            start_date=data_d.index.min().date(),
                            end_date=data_d.index.max().date(),
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
                        id="sales-chart-period", config={"displayModeBar": False}
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=dcc.Graph(
                id="forecast-chart", config={"displayModeBar": False}
            ),
            className="wrapperSecond",
        ),
        #html.Div(
            #children=dcc.Graph(
                #id="indicators-chart", config={"displayModeBar": False}
            #),
            #className="wrapperSecond",
        #),
    ]
)

# Callback do botão de baixar previsão
'''
@app.callback(
    Output("download", "data"),
    [Input("bt-download", "n_clicks"), Input("product-filter", "value"), Input("frequency-selector", "value")]
)
def download_forecast(n_clicks, product, frequency):
    if n_clicks is None:
        return no_update
        
    path = "previsao/forecasts/" + frequency + "/" + product.replace(" ", "_").replace("/", "_") + ".csv"
    try:
        forecast = pd.read_csv(path)
        forecast.index = pd.to_datetime(forecast['ds'])
        return send_data_frame(forecast.to_csv, filename="Previsao_" + product.replace(" ", "_").replace("/", "_") + ".csv")
    except:
        return html.Div("Um erro ocorreu ao tentar obter a previsão!")
'''

# Callback da seleção de categoria
@app.callback(
    [Output("product-filter", "options"), Output("product-filter", "value")],
    [Input("category-filter", "value")]
)
def update_products(category):
    return [{"label": product, "value": product} for product in categories_dict[category]], categories_dict[category][0]

# Callback da seleção de produto, frequência, e data
@app.callback(
# Lembrete: Se tiver mais de uma chamada de Output(...) colocar em uma lista as multiplas chamadas
    #[Output("sales-chart-cumsum", "figure"), Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")],
    [Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")], # Output("indicators-chart", "figure")
    [Input("product-filter", "value"), Input("frequency-selector", "value"), Input("date-range", "start_date"), Input("date-range", "end_date")]
)
def update_charts(product, frequency, start_date, end_date):
    if frequency == 'D':
        mask = (
        (data_d.index >= start_date)
        & (data_d.index <= end_date)
        )
        filtered_data = data_d.loc[mask, :]
    elif frequency == 'W-MON':
        mask = (
        (data_w.index >= start_date)
        & (data_w.index <= end_date)
        )
        filtered_data = data_w.loc[mask, :]
    else: # frequency == 'M'
        mask = (
        (data_m.index >= start_date)
        & (data_m.index <= end_date)
        )
        filtered_data = data_m.loc[mask, :]
        
    filtered_data = filtered_data.resample(frequency).sum()
    
    sales_period_chart_figure = get_sales_figure(filtered_data, product)
    forecast_chart_figure, forecast = get_forecast_figure(filtered_data, product, '2021-03-16', frequency) 
    #indicators_chart_figure = get_indicators_figure(filtered_data, forecast, product, '2021-03-16')

    return sales_period_chart_figure, forecast_chart_figure#, indicators_chart_figure
