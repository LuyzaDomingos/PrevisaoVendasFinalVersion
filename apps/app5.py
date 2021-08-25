# Aplicativo 5 (relatorio de categoria)
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
stores = ['Patos II', 'Pombal', 'Itaporanga', 'Matriz', 'Patos I', 'Ico',
 'Patos IV', 'Sousa II', 'Pianco', 'Patos III', 'Iguatu', 'teste',
 'Sousa I', 'Joao Dourado', 'Irece I', 'Jacobina', 'Irece II', 'Itambe',
 'Goiana', 'Cabedelo', 'Mangabeira Shopping', 'Bancarios', 'Timbauba', 'Bayeux',
 'Goiana 2', 'CABEDELO BR', 'Sta. Rita', 'Manaira', 'Lagoa', 'Mangabeira',
 'Barao', 'Geisel', 'Alhandra', 'Itabaiana', 'Sto. Elias', 'Aristides Lobo',
 'Picui', 'Guarabira', 'Campina Grande IV', 'AREIA', 'Campina Grande II', 'Esperanca',
 'Mamanguape', 'Campina Grande I', 'Alagoa Grande', 'Monteiro 2', 'Cuite', 'Campina Grande III',
 'Queimadas', 'Soledade', 'Lagoa Seca', 'Guarabira II', 'Sape', 'Caruaru',
 'Solanea', 'Monteiro']
dates = ['3/2021', '2/2021', '1/2021', 
        '12/2020', '11/2020', '10/2020', '9/2020', '8/2020', '7/2020', '6/2020', '5/2020', '4/2020', '3/2020', '2/2020', '1/2020', 
        '12/2019', '11/2019', '10/2019', '9/2019', '8/2019', '7/2019', '6/2019', '5/2019', '4/2019', '3/2019', '2/2019', '1/2019', 
        '12/2018', '11/2018', '10/2018', '9/2018', '8/2018', '7/2018', '6/2018', '5/2018', '4/2018', '3/2018', '2/2018', '1/2018']

#categories = list(json.load(open('previsao/subcategorias.json')).keys())
#categories.insert(0, 'GERAL')
# Carregar dados de resumo
data_stores_regions = pd.read_csv('previsao/Resumo Lojas.csv', index_col=0)
data_stores_regions.index = pd.to_datetime(data_stores_regions.index)
data_stores_regions_m = data_stores_regions.resample('M').sum()

def get_layout(actual_category='ELETRO LINHA BRANCA'):
    return html.Div(children=[
        #dcc.Store(id='bt-memory', storage_type='memory', data='bt-geral'),
            html.Div(children=[
                    html.Br(),
                    html.H1(children="Relatório de " + actual_category, className="header-title"),
                    html.P(children="Visualização das vendas por região, loja, ou geral. Os dados são fictícios. WIP.", className="header-description"),
                    #html.Div([
                    #html.Button('Geral', id='bt-geral', n_clicks=0, className='flex-item'),
                    #html.Button('Região', id='bt-region', n_clicks=0, className='flex-item'),
                    #html.Button('Lojas', id='bt-store', n_clicks=0, className='flex-item'),
                    #], className="flex-container center"),
                    dcc.Link('Voltar à previsão por categoria', href='app2', className='link'),
                ],
                className="header",
        ),
        html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Mês", className="menu-title"),
                            dcc.Dropdown(
                                id="smonth-selector",
                                options=[{"label": date, "value": date} for date in dates],
                                value="3/2021",
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),
                    #html.Div(
                    #    children=[
                            #html.Div(children="Categoria", className="menu-title"),
                            #dcc.Dropdown(
                            #    id="scategory-selector",
                            #    options=[{"label": key, "value": key} for key in categories],
                            #    value="GERAL",
                            #    clearable=False,
                            #    className="dropdown",
                            #),
                    #    ]
                    #),
                ],
                className="menu", style={'height': '90px', 'padding-top': '12px'}
            ),
            html.Div(
                id="critical-items-list",
                className="wrapper",
                style={'margin-top': '10px', 'max-width': '1320px'},
            ),
        ]
    )

@app.callback([Output('critical-items-list', 'children'), Output('critical-items-list', 'style')],
            [Input("smonth-selector", "value")])
def update_list(*args):
    # Obter o mês e ano da entrada
#    split = args[4].split('/')
#    year = int(split[1])
#    month = int(split[0])
#    # Obter os produtos
#    if args[3] == 'GERAL':
#        products = categories[1:]
#    else:
#        products = app1.categories_dict[args[3]]
#    # Definir se o callback foi ativado por um botão
#    ctx = callback_context
#    if not ctx.triggered or not any(args): # Caso entre aqui é por ter sido o startup do aplicativo
#        #return ['flex-item' for _ in range(3)], no_update, no_update
#        return get_general_panel(data=app1.data_m, month=month, year=year, category=args[3], products=products), {'max-width': '1320px'}, no_update
#
#    # Obter o id do botão selecionado (ou não, caso não tenha sido um que disparou o callback)
#    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#    if button_id == args[5]: # Foi clicado no mesmo botão
#        return no_update, no_update, no_update
#    # Atualizar as saídas
#    if button_id == "bt-geral":
#        return get_general_panel(data=app1.data_m, month=month, year=year, category=args[3], products=products), {'max-width': '1320px'}, "bt-geral"
#    if button_id == "bt-store":
#        return get_list(app2.facts, month=month, year=year, items=stores, sales_panel=True, sales_data=data_stores_regions_m, sales_panel_category=args[3]), {'max-width': '1024px'}, "bt-store"
#    if button_id == "bt-region":
#        return get_list(app2.facts, month=month, year=year, items=regions, sales_panel=True, sales_data=data_stores_regions_m,  sales_panel_category=args[3]), {'max-width': '1024px'}, "bt-region"
#    else: # O input que causou o callback não foi um botão
#        if args[5] == "bt-geral":
#            return get_general_panel(data=app1.data_m, month=month, year=year, category=args[3], products=products), {'max-width': '1320px'}, no_update
#        if args[5] == "bt-store":
#            return get_list(app2.facts, month=month, year=year, items=stores, sales_panel=True, sales_data=data_stores_regions_m,  sales_panel_category=args[3]), {'max-width': '1024px'}, no_update
#        if args[5] == "bt-region":
#            return get_list(app2.facts, month=month, year=year, items=regions, sales_panel=True, sales_data=data_stores_regions_m,  sales_panel_category=args[3]), {'max-width': '1024px'}, no_update

    return no_update, no_update
