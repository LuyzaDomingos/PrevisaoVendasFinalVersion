# Aplicativo 4 (painel de vendas)
import pandas as pd
import json

import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import no_update, callback_context

from app import app
from apps import app1, app2

from util import get_list, get_general_panel

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
dates = ['3/2021', '2/2021', '1/2021', 
        '12/2020', '11/2020', '10/2020', '9/2020', '8/2020', '7/2020', '6/2020', '5/2020', '4/2020', '3/2020', '2/2020', '1/2020', 
        '12/2019', '11/2019', '10/2019', '9/2019', '8/2019', '7/2019', '6/2019', '5/2019', '4/2019', '3/2019', '2/2019', '1/2019', 
        '12/2018', '11/2018', '10/2018', '9/2018', '8/2018', '7/2018', '6/2018', '5/2018', '4/2018', '3/2018', '2/2018', '1/2018']

categories = list(json.load(open('previsao/subcategorias.json')).keys())
categories.insert(0, 'GERAL')

layout = html.Div(children=[
    dcc.Store(id='bt-memory', storage_type='memory', data='none'),
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
                            options=[{"label": date, "value": date} for date in dates],
                            value="3/2021",
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
                            value="GERAL",
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
            style={'margin-top': '10px', 'max-width': '1320px'},
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

@app.callback([Output('items-list', 'children'), Output('items-list', 'style'), Output('bt-memory', 'data')],
            [Input('bt-geral', 'n_clicks'), Input('bt-store', 'n_clicks'), Input('bt-region', 'n_clicks'), Input("category-selector", "value"), Input("month-selector", "value"), Input('bt-memory', 'data')])
def update_list(*args):
    ctx = callback_context
    if not ctx.triggered or not any(args):
        return ['flex-item' for _ in range(3)], no_update, no_update
    # Obter o id do botão selecionado (ou não, caso não tenha sido um que disparou o callback)    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # Obter o mês e ano da entrada
    split = args[4].split('/')
    year = int(split[1])
    month = int(split[0])
    # Obter os produtos
    if args[3] == 'GERAL':
        products = categories[1:]
    else:
        products = app1.categories_dict[args[3]]

    # Atualizar as saídas
    if button_id == "bt-geral":
        return get_general_panel(data=app1.data_m, month=month, year=year, category=args[3], products=products), {'max-width': '1320px'}, "bt-geral"
    if button_id == "bt-store":
        return get_list(app2.facts, items=stores, sales_panel=True), {'max-width': '1024px'}, "bt-store"
    if button_id == "bt-region":
        return get_list(app2.facts, items=regions, sales_panel=True), {'max-width': '1024px'}, "bt-region"
    else: # O input que causou o callback não foi um botão
        if args[5] == "bt-geral":
            return get_general_panel(data=app1.data_m, month=month, year=year, category=args[3], products=products), {'max-width': '1320px'}, no_update
        if args[5] == "bt-store":
            return get_list(app2.facts, items=stores, sales_panel=True), {'max-width': '1024px'}, no_update
        if args[5] == "bt-region":
            return get_list(app2.facts, items=regions, sales_panel=True), {'max-width': '1024px'}, no_update

    return no_update, no_update, no_update