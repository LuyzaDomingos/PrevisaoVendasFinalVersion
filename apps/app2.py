import json
import pandas as pd

import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

suppliers_dict = json.load(open('previsao/fornecedores2.json'))

df = px.data.tips()
fig = px.bar(df, x="sex", y="total_bill",
             color='smoker', barmode='group',
             height=400)

layout = html.Div(children=[
    html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Previsão de vendas", className="header-title"),
                html.P(children="Visualização e previsão de séries temporais referentes à vendas de produtos", className="header-description"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
            ],
            className="header",
        ),
    html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Fornecedor", className="menu-title"),
                        dcc.Dropdown(
                            id="supplier-filter",
                            options=[{"label": key, "value": key} for key in list(suppliers_dict.keys())],
                            value="ESMALTEC",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
])

@app.callback(
    [Output('app-1-display-value', 'children')],
    [Input('app-1-dropdown', 'value')]
    )
def display_value(value):
    return 'You have selected "{}"'.format(value)