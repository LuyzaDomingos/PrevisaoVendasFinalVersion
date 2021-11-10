import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import no_update

from apps import app1, app2
from app import app
from util import get_sales_figure, get_top_list, draw_top_list

import json


def get_layout(actual_category="ELETRO LINHA BRANCA"):
    return html.Div(
        children=[
            dcc.Store(
                id="memory",
                storage_type="memory",
                data=get_top_list(
                    app1.data_d, app2.cats[actual_category]
                ).to_json(),
            ),
            html.Div(
                children=[
                    html.H1(
                        children="Panorama de " + actual_category,
                        className="header-title",
                    ),
                    html.P(
                        children="Visualização da série temporal da caterogia e top 5",
                        className="header-description",
                    ),
                    dcc.Link(
                        "Voltar à previsão por categoria",
                        href="app2",
                        className="link",
                    ),
                ],
                className="header category",
            ),
            html.Div(
                children=[
                    html.Div(
                        id="top5-table",
                        children=[
                            html.P(
                                children="Top 5 produtos de "
                                + actual_category,
                                className="title",
                            ),
                            draw_top_list(
                                app1.data_d, app2.cats[actual_category]
                            ),
                        ],
                        className="left white",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id="cat-sales-chart",
                            config={"displayModeBar": False},
                            style={"height": "100%", "width": "100%"},
                            figure=get_sales_figure(
                                app1.data_d, actual_category
                            ),
                        ),
                        className="right",
                    ),
                ],
                className="container",
            ),
        ]
    )


@app.callback(
    Output("cat-sales-chart", "figure"),
    [Input("top-table", "active_cell"), Input("memory", "data")],
)
def update_chart(active_cell, data):
    if active_cell:  # Uma célula foi selecionada
        return get_sales_figure(
            app1.data_d, pd.read_json(data).iloc[active_cell["row"]]["Produto"]
        )
    # Nada foi selecionado
    return no_update
