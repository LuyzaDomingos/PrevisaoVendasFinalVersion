# Aplicativo 4 (painel de vendas)
import pandas as pd
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import no_update, callback_context

from app import app
from apps import app2

from util import get_list

actual_category = 'ELETRO LINHA BRANCA'
regions = ['SERTAO', 'BAHIA', 'LITORAL', 'BREJO']
stores = ['Ico', 'Jacobina', 'Lagoa', 'Campina Grande I', 'Bayeux',
       'Esperanca', 'Irece I', 'Mangabeira Shopping', 'Patos I', 'Matriz',
       'Patos II', 'Campina Grande III', 'Itambe', 'Campina Grande II',
       'Mangabeira', 'Aristides Lobo', 'Sape', 'Sta. Rita', 'Iguatu',
       'Pombal', 'Itaporanga', 'Mamanguape', 'Sousa I', 'Timbauba',
       'Joao Dourado', 'Goiana', 'Cuite', 'Queimadas', 'Irece II',
       'Solanea', 'Guarabira', 'Cabedelo', 'Alagoa Grande', 'AREIA',
       'Bancarios', 'Sousa II', 'Barao', 'Soledade', 'Guarabira II',
       'Goiana 2', 'Geisel', 'Picui', 'Alhandra', 'Itabaiana',
       'Lagoa Seca', 'Campina Grande IV', 'Monteiro', 'Patos III',
       'Pianco', 'Sto. Elias', 'CD Cabedelo', 'Monteiro 2', 'Caruaru',
       'Manaira', 'CABEDELO BR', 'Patos IV', 'teste']
       
categories = list(json.load(open('previsao/subcategorias.json')).keys())
categories.insert(0, '-')

data = pd.read_csv("previsao/geral.csv", index_col=0)
data.fillna(value=0, inplace=True)
data.index = pd.to_datetime(data.index)
data = data[:'2021-03-12']

layout = html.Div(children=[
    html.Div(children=[
                html.Br(),
                html.H1(children="Painel de Vendas", className="header-title"),
                html.P(children="Visualização das vendas por região, loja, ou geral. Os dados são fictícios. WIP.", className="header-description"),
                html.Div([
                html.Button('Geral', id='bt-geral', n_clicks=0, className='flex-item'),
                html.Button('Região', id='bt-region', n_clicks=0, className='flex-item'),
                html.Button('Lojas', id='bt-store', n_clicks=0, className='flex-item'),
                ], className="flex-container center"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
            ],
            className="header",
    ),
    html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Mês", className="menu-title"),
                        dcc.Dropdown(
                            id="month-selector",
                            options=[{"label": str(key) + "/2021", "value": str(key)} for key in range(1, 13)],
                            value="3",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Categoria", className="menu-title"),
                        dcc.Dropdown(
                            id="category-selector",
                            options=[{"label": key, "value": key} for key in categories],
                            value="-",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            id="items-list",
            className="wrapper",
        ),
    ]
)
buttons = ['bt-geral', 'bt-store', 'bt-region']
@app.callback([Output('bt-geral', 'className'),
              Output('bt-store', 'className'),
              Output('bt-region', 'className')],
              [Input('bt-geral', 'n_clicks'),
              Input('bt-store', 'n_clicks'),
              Input('bt-region', 'n_clicks')])
def set_active(*args):
    ctx = callback_context
    
    if not ctx.triggered or not any(args):
        return ['flex-item' for _ in range(3)]
        
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    styles = []
    for button in buttons:
        if(button == button_id):
            styles.append('flex-item selected')
        else:
            styles.append('flex-item')
            
    return styles

@app.callback(Output('items-list', 'children'),
              [Input('bt-geral', 'n_clicks'),
              Input('bt-store', 'n_clicks'),
              Input('bt-region', 'n_clicks')])
def update_list(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return ['flex-item' for _ in range(3)]
        
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "bt-geral":
        return None
    if button_id == "bt-store":
        return get_list(app2.facts, items=stores, sales_panel=True)
    if button_id == "bt-region":
        return get_list(app2.facts, items=regions, sales_panel=True)
