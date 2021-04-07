import json
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from random import randint

suppliers_dict = json.load(open('previsao/fornecedores2.json'))

def foo():
    child = []
    i = 0
    for supplier in suppliers_dict:
        i += 1
        if i > 10:
            break
        fig = go.Figure()
        fig.update_layout(height=80, margin=dict(l=40, r=40, t=8, b=8))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 999),
            title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
            delta = {'reference': randint(0, 999), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 99),
            #title = {'text': "<span style=='font-size:14px'>Estoque atual</span>"},
            title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
            delta = {'reference': randint(0, 99), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 1}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = randint(0, 9999999),
            #title = {'text': "<span style=='font-size:14px'>Valor das vendas</span>"},
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
        child.append(html.Div(children=[dcc.Link("        📈  " + supplier, href='index', className='link white-bg'), dcc.Graph(id="sales-chart-period-"+supplier, config={"displayModeBar": False}, figure=fig)], className="card small-margin"))

    return child

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
            children=foo(),
            className="wrapper",
        ),
])

@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)