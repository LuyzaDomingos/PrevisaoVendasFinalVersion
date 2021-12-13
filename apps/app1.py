# Aplicativo 1 (Previsão por produtos)
import json
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html

# Dependências do Dash
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash import no_update, callback_context

# API de previsão de séries temporais
from fbprophet import Prophet

# Funções de plotagem
from util import (
    get_forecast_figure,
    get_sales_figure,
    get_indicators_figure,
    get_stocks_figure,
    get_sales_loss_figure,
    heroku,
)

from app import app

# Função para leitura de dados
def read_data(path, fillna=False, end_date="2021-03-12"):
    data = pd.read_csv(path, index_col=0)
    if fillna is True:
        data.fillna(value=0, inplace=True)
    data.index = pd.to_datetime(data.index)
    data = data[:end_date]

    return data


# Leitura dos dados, amostragem diária
data_d = read_data("previsao/geral2.csv", fillna=True)
# Amostragem semanal
data_w = data_d.resample("W-MON").sum()
# Amostragem mensal
data_m = data_d.resample("M").sum()
# Dados de estoque
data_stock = read_data("previsao/estoque2.csv")
# Dados de ruptura
data_loss = read_data("previsao/ruptura_geral.csv")
# Ruptura versão 2 WIP
# Para efeitos de teste, trabalharemos no momento com os dados da loja da lagoa
# Vendas da Loja
df_sales = read_data("data/sales/Lagoa_2.csv")
# Estoque da Loja
df_stock = read_data("data/stock/Lagoa_2.csv")
# Estoque de segurança do CD
security_dc = read_data("data/ES CBO.csv")
# Estoque de segurança das lojas abastecidas pelo CD
security_dc_stores = read_data("data/ES CBO Lojas.csv")
# Estoque de segurança da Loja
security_store = read_data("data/ES Lagoa.csv")
# Ruptura de Loja
data_loss_store = read_data("data/Loja#Lagoa.csv")
# Ruptura de Compra
data_loss_purchase = read_data("data/Compra#Lagoa.csv")
# Ruptura de Estoque
data_loss_stock = read_data("data/Estoque#Lagoa.csv")
# Dicionário de categorias
categories_dict = json.load(open("previsao/classificacao.json"))
# Dicionário de frequências
freq_dict = {"Diário": "D", "Semanal": "W-MON", "Mensal": "M"}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Avenir:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

layout = html.Div(
    children=[
        dcc.Store(id="bt-memory-pred", storage_type="memory", data="bt-sales"),
        html.Div(
            children=[
                # html.P(children="📈", className="header-emoji"),
                html.Br(),
                html.H1(
                    children="Previsão por Produtos", className="header-title"
                ),
                html.P(
                    children="Visualização e previsão de séries temporais referentes à vendas e estoques de produtos",
                    className="header-description",
                ),
                html.Div(
                    [
                        html.Button(
                            "Vendas",
                            id="bt-sales",
                            n_clicks=0,
                            className="flex-item",
                        ),
                        html.Button(
                            "Estoque",
                            id="bt-stock",
                            n_clicks=0,
                            className="flex-item",
                        ),
                    ],
                    className="flex-container center",
                ),
                dcc.Link(
                    "Voltar à página inicial", href="index", className="link"
                ),
                # html.Button("Baixe a previsão (.csv)", id="bt-download", className="bt"),
                # Download(id="download"),
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
                            options=[
                                {"label": key, "value": key}
                                for key in list(categories_dict.keys())
                            ],
                            value="AR E VENTILACAO",
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
                                for product in categories_dict[
                                    "AR E VENTILACAO"
                                ]
                            ],
                            value="VENTILADOR 30CM NV-15 6P BR 220V",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Frequência", className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="frequency-selector",
                            options=[
                                {"label": key, "value": value}
                                for key, value in freq_dict.items()
                            ],
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
                            className="menu-title",
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
                        id="sales-chart-period",
                        config={"displayModeBar": False},
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
        # html.Div(
        # children=dcc.Graph(
        # id="indicators-chart", config={"displayModeBar": False}
        # ),
        # className="wrapperSecond",
        # ),
    ]
)

# Callback do botão de baixar previsão
"""
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
"""

# Callback de mostrar o botão atualmente selecionado
buttons = ["bt-sales", "bt-stock"]


@app.callback(
    [Output("bt-sales", "className"), Output("bt-stock", "className")],
    [Input("bt-sales", "n_clicks"), Input("bt-stock", "n_clicks")],
)
def set_active(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return [
            "flex-item" if x > 0 else "flex-item selected" for x in range(2)
        ]

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    styles = []
    for button in buttons:
        if button == button_id:
            styles.append("flex-item selected")
        else:
            styles.append("flex-item")

    return styles


# Callback da seleção de categoria
@app.callback(
    [Output("product-filter", "options"), Output("product-filter", "value")],
    [Input("category-filter", "value")],
)
def update_products(category):
    return [
        {"label": product, "value": product}
        for product in categories_dict[category]
    ], categories_dict[category][0]


# Callback da seleção de produto, frequência, e data
@app.callback(
    # Lembrete: Se tiver mais de uma chamada de Output(...) colocar em uma lista as multiplas chamadas
    # [Output("sales-chart-cumsum", "figure"), Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")],
    [
        Output("sales-chart-period", "figure"),
        Output("forecast-chart", "figure"),
        Output("bt-memory-pred", "data"),
    ],  # Output("indicators-chart", "figure")
    [
        Input("product-filter", "value"),
        Input("frequency-selector", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("bt-sales", "n_clicks"),
        Input("bt-stock", "n_clicks"),
        Input("bt-memory-pred", "data"),
    ],
)
def update_charts(
    product,
    frequency,
    start_date,
    end_date,
    bt_sales_nclicks,
    bt_stock_nclicks,
    memory,
):
    # Reorganizar os dados segundo a frequência selecionada
    if frequency == "D":
        mask = (data_d.index >= start_date) & (data_d.index <= end_date)
        filtered_data = data_d.loc[mask, :]
    elif frequency == "W-MON":
        mask = (data_w.index >= start_date) & (data_w.index <= end_date)
        filtered_data = data_w.loc[mask, :]
    else:  # frequency == 'M'
        mask = (data_m.index >= start_date) & (data_m.index <= end_date)
        filtered_data = data_m.loc[mask, :]

    filtered_data = filtered_data.resample(frequency).sum()
    # Obter o id do botão selecionado (ou não, caso não tenha sido um que disparou o callback)
    ctx = callback_context
    if not ctx.triggered or not any(
        [bt_sales_nclicks, bt_stock_nclicks]
    ):  # Caso entre aqui é por ter sido o startup do aplicativo
        return (
            get_sales_figure(filtered_data, product),
            get_forecast_figure(
                filtered_data, product, "2021-03-16", frequency
            ),
            no_update,
        )

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # Mostrar o tipo de gráfico selecionado
    if button_id == "bt-sales":  # O botão selecionado é o de vendas
        return (
            get_sales_figure(filtered_data, product),
            get_forecast_figure(
                filtered_data, product, "2021-03-16", frequency
            ),
            "bt-sales",
        )
    elif button_id == "bt-stock":  # O botão selecionado é o de estoque
        # mask = (
        #    (data_d.index >= start_date)
        #    & (data_d.index <= end_date)
        #    )
        # filtered_data = data_d.loc[mask, :]
        # filtered_data = filtered_data.resample('M').sum()

        mask = (data_stock.index >= start_date) & (
            data_stock.index <= end_date
        )
        filtered_data_stock = data_stock.loc[mask, :]
        mask = (data_loss.index >= start_date) & (data_loss.index <= end_date)
        filtered_data_sales = df_sales.loc[mask, :]
        filtered_data_stock = df_stock.loc[mask, :]
        filtered_data_security_store = security_store.loc[mask, :]
        filtered_data_security_dc = security_dc.loc[mask, :]
        filtered_data_security_dc_stores = security_dc_stores.loc[mask, :]
        filtered_data_loss_store = data_loss_store.loc[mask, :]
        filtered_data_loss_stock = data_loss_stock.loc[mask, :]
        filtered_data_loss_purchase = data_loss_purchase.loc[mask, :]

        return (
            get_stocks_figure(
                filtered_data_stock, filtered_data, product, frequency
            ),
            get_sales_loss_figure(
                filtered_data_sales,
                filtered_data_stock,
                filtered_data_security_store,
                filtered_data_security_dc,
                filtered_data_security_dc_stores,
                filtered_data_loss_purchase,
                filtered_data_loss_store,
                filtered_data_loss_stock,
                product,
                freq=frequency,
            ),
            "bt-stock",
        )
    else:  # O callback não foi gerado por um botão
        if memory == "bt-sales":
            return (
                get_sales_figure(filtered_data, product),
                get_forecast_figure(
                    filtered_data, product, "2021-03-16", frequency
                ),
                no_update,
            )
        elif memory == "bt-stock":
            # mask = (
            #    (data_d.index >= start_date)
            #    & (data_d.index <= end_date)
            #    )
            # filtered_data = data_d.loc[mask, :]
            # filtered_data = filtered_data.resample('M').sum()

            mask = (data_stock.index >= start_date) & (
                data_stock.index <= end_date
            )
            filtered_data_stock = data_stock.loc[mask, :]
            mask = (data_loss.index >= start_date) & (
                data_loss.index <= end_date
            )
            filtered_data_sales = df_sales.loc[mask, :]
            filtered_data_stock = df_stock.loc[mask, :]
            filtered_data_security_store = security_store.loc[mask, :]
            filtered_data_security_dc = security_dc.loc[mask, :]
            filtered_data_security_dc_stores = security_dc_stores.loc[mask, :]
            filtered_data_loss_store = data_loss_store.loc[mask, :]
            filtered_data_loss_stock = data_loss_stock.loc[mask, :]
            filtered_data_loss_purchase = data_loss_purchase.loc[mask, :]

            return (
                get_stocks_figure(
                    filtered_data_stock, filtered_data, product, frequency
                ),
                get_sales_loss_figure(
                    filtered_data_sales,
                    filtered_data_stock,
                    filtered_data_security_store,
                    filtered_data_security_dc,
                    filtered_data_security_dc_stores,
                    filtered_data_loss_purchase,
                    filtered_data_loss_store,
                    filtered_data_loss_stock,
                    product,
                    freq=frequency,
                ),
                no_update,
            )
        else:
            return no_update, no_update, no_update
