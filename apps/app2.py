import json
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from util import get_list

cats = json.load(open('previsao/subcategorias.json'))
facts = pd.read_csv("previsao/fatos.csv")

sort_dict = {
    'Vendas previstas': 'Venda prevista',
    'Estoque atual': 'Estoque atual',
    'Valor das vendas': 'Valor venda',
    'Ordem alfabética': 'Categoria'
}
order_dict = {
    'Crescente': 1,
    'Decrescente': 0
}

layout = html.Div(children=[
    html.Div(children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Listagem de categorias", className="header-title"),
                html.P(children="Indicadores de vendas, estoque e valores. Os dados são fictícios. WIP.", className="header-description"),
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
                            value="Venda prevista",
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
                            value=0,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu full",
        ),
    html.Div(
            id='class-list',
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output('class-list', 'children')],
    [Input('criteria-selector', 'value'), Input('order-selector', 'value')]
    )
def sort_list(criteria, order):
    return [get_list(facts, sort_by=criteria, ascending=order)]
