import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import no_update

from apps import app1, app2
from app import app
from util import get_sales_figure, get_top_list, draw_top_list

actual_category = 'ELETRO LINHA BRANCA'

layout = html.Div(children=[
    html.Div(children=[
                html.H1(children="Panorama de " + actual_category, className="header-title"),
                html.P(children="Visualização da série temporal da caterogia e top 5", className="header-description"),
                dcc.Link('Voltar à página inicial', href='index', className='link'),
            ],
            className="header category",
    ),
    html.Div(children=[
                    html.Div(id='top5-table', children=[html.P(children="Top 5 produtos de " + actual_category, className="title"), draw_top_list(app1.data_d, app2.cats[actual_category])], className="left white"),
                html.Div(children=dcc.Graph(id="cat-sales-chart", config={"displayModeBar": False}, style={"height": "100%", "width": "100%"}, figure=get_sales_figure(app1.data_d,  actual_category)), className="right")
            ],
        className="container",
    ),
    ]
)
a = get_top_list(app1.data_d, app2.cats[actual_category])

@app.callback(
    Output('cat-sales-chart', 'figure'),
    [Input('top-table', 'active_cell')])
def update_chart(active_cell):
    if active_cell: # Uma célula foi selecionada
        return get_sales_figure(app1.data_d,  a.iloc[active_cell['row']]['Produto'])
    # Nada foi selecionado
    return no_update
