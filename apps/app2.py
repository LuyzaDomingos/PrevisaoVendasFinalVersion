# Aplicativo 2 (Previsão por categoria)
import json
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import no_update
# Bibliotecas para download dos dados
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame, send_bytes
import xlsxwriter
from app import app

from util import get_list

cats = json.load(open('previsao/classificacao.json'))
facts = pd.read_csv("previsao/fatos.csv")

sort_dict = {
    'Vendas previstas': 'Venda prevista',
    'Estoque atual': 'Estoque atual',
    'Cobertura de Estoque': 'Cobertura',
    'Ordem alfabética': 'Categoria'
}
order_dict = {
    'Crescente': 1,
    'Decrescente': 0
}

layout = html.Div(children=[
    html.Div(children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Previsão por Categoria", className="header-title"),
                html.P(children="Indicadores de previsão de vendas, estoque, cobertura, e comparação com o mês anterior.", className="header-description"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
                html.Button("Baixe a previsão", id="bt-download", className="bt"),
                Download(id="download"),
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
# Callback de ordenação
@app.callback(
    [Output('class-list', 'children')],
    [Input('criteria-selector', 'value'), Input('order-selector', 'value')]
    )
def sort_list(criteria, order):
    return [get_list(facts, sort_by=criteria, ascending=order)]
    
# Callback de download
@app.callback(
    Output("download", "data"),
    [Input("bt-download", "n_clicks")]
)
def download_forecast(n_clicks):
    def to_xlsx(bytes):
        writer = pd.ExcelWriter(bytes, engine='xlsxwriter')
        facts.to_excel(writer, index=False, sheet_name='Fatos')
        writer.save()
    
    if n_clicks is None:
        return no_update
    
    return send_bytes(to_xlsx, filename="Tabela Fatos.xlsx")
