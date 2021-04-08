import json
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from util import get_list

cats = json.load(open('previsao/subcategorias.json'))

sort_dict = {
    'Vendas previstas': 'Vendas',
    'Estoque disponível': 'Estoque',
    'Valor das vendas': 'Valor',
    'Ordem alfabética': 'A-Z'
}
order_dict = {
    'Crescente': 1,
    'Decrescente': 0
}

child = get_list(cats)

layout = html.Div(children=[
    html.Div(children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Previsão de Vendas", className="header-title"),
                html.P(children="Visualização e Previsão de séries temporais referentes à vendas de produtos", className="header-description"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
            ],
            className="header",
        ),
    html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Ordernar por", className="menu-title"),
                        dcc.Dropdown(
                            id="criteria-selector",
                            options=[{"label": key, "value": value} for key, value in sort_dict.items()],
                            value="A-Z",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Ordem", className="menu-title"),
                        dcc.Dropdown(
                            id="order-selector",
                            options=[{"label": key, "value": value} for key, value in order_dict.items()],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu full",
        ),
    html.Div(
            children=child,
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output('app-1-display-value', 'children')],
    [Input('app-1-dropdown', 'value')]
    )
def display_value(value):
    return 'You have selected "{}"'.format(value)