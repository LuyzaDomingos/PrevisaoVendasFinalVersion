# Aplicativo 6 (Configurações)
import json
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Dependências do Dash
from dash.dependencies import Input, Output, State
from dash import no_update, callback_context
from dash_table import DataTable

from app import app
from apps import app4

store_selector_dropdown = dcc.Dropdown(
    id="store-selector",
    options=[{"label": store, "value": store} for store in app4.stores],
    value="Alagoa Grande",
    clearable=False,
    className="dropdown",
)

bt_save = html.Div(
    [
        dbc.Button(
            "Salvar",
            id="bt-save-active",
            n_clicks=0,
            className="flex-item",
            style={"width": "180px", "backgroundColor": "rgb(255, 255, 255)"},
        ),
        dbc.Modal(
            [
                dbc.ModalBody("Alterações salvas"),
            ],
            id="modal-save",
            size="sm",
            is_open=False,
        ),
    ]
)


def get_table(search=None):
    active = json.load(open("previsao/ativo.json"))

    products = active["0"] + active["1"]

    active_t = {}
    for product in products:
        if product in active["0"]:
            active_t[product] = "Não"
        else:
            active_t[product] = "Sim"

    active_df = pd.DataFrame(active_t.items(), columns=["Produto", "Ativo"])

    return DataTable(
        id="product-table",
        columns=[
            {"name": "Produto", "id": "Produto", "editable": False},
            {"name": "Ativo", "id": "Ativo", "editable": True},
        ],
        data=active_df.to_dict("records"),
        style_as_list_view=True,
        filter_action="native",
        filter_query="",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=15,
        style_data={
            "textAlign": "center",
            "whiteSpace": "normal",
            "overflowY": "auto",
            "fontFamily": "Avenir",
            "fontSize": "16px",
            "padding": "12px",
        },
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            "textAlign": "center",
            "fontFamily": "Avenir",
            "fontSize": "16px",
            "padding": "12px",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "rgb(248, 248, 248)",
            },
        ],
        style_cell_conditional=[
            {"if": {"column_id": "Ativo"}, "width": "30%"},
        ],
    )


layout = html.Div(
    children=[
        dcc.Store(
            id="bt-memory-settings",
            storage_type="memory",
            data="bt-product-active",
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(children="Configurações", className="header-title"),
                html.P(
                    children="Edição da lista de produtos ativos, e seleção de loja.",
                    className="header-description",
                ),
                html.Div(
                    [
                        html.Button(
                            "Produtos Ativos",
                            id="bt-product-active",
                            n_clicks=0,
                            className="flex-item",
                            style={"width": "180px"},
                        ),
                        html.Button(
                            "Selecionar Loja",
                            id="bt-select-store",
                            n_clicks=0,
                            className="flex-item",
                            style={"width": "180px"},
                        ),
                    ],
                    className="flex-container center",
                ),
                dcc.Link(
                    "Voltar à página inicial", href="index", className="link"
                ),
            ],
            className="header",
        ),
        html.Div(
            id="settings-menu",
            className="menu",
            style={"height": "60px", "padding-top": "12px"},
        ),
        html.Div(
            id="items-list-settings",
            className="wrapper",
            style={"margin-top": "10px", "max-width": "1320px"},
        ),
    ]
)

buttons = ["bt-product-active", "bt-select-store"]


@app.callback(
    [
        Output("bt-product-active", "className"),
        Output("bt-select-store", "className"),
    ],
    [
        Input("bt-product-active", "n_clicks"),
        Input("bt-select-store", "n_clicks"),
    ],
)
def set_active(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return [
            "flex-item" if x > 0 else "flex-item selected" for x in range(2)
        ]

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    styles = []
    for button in buttons:
        if button == button_id:
            styles.append("flex-item selected")
        else:
            styles.append("flex-item")

    return styles


@app.callback(
    [
        Output("settings-menu", "children"),
        Output("items-list-settings", "children"),
        Output("items-list-settings", "style"),
        Output("bt-memory-settings", "data"),
    ],
    [
        Input("bt-product-active", "n_clicks"),
        Input("bt-select-store", "n_clicks"),
        Input("bt-memory-settings", "data"),
    ],
)
def update_list(*args):
    # Definir se o callback foi ativado por um botão
    ctx = callback_context
    if not ctx.triggered or not any(
        args
    ):  # Caso entre aqui é por ter sido o startup do aplicativo
        return [bt_save], get_table(), no_update, no_update

    # Obter o id do botão selecionado (ou não, caso não tenha sido um que disparou o callback)
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == args[2]:  # Foi clicado no mesmo botão
        return no_update, no_update, no_update, no_update
    # Atualizar as saídas
    if button_id == "bt-product-active":
        return [bt_save], get_table(), no_update, "bt-product-active"
    if button_id == "bt-select-store":
        return [store_selector_dropdown], None, no_update, "bt-select-store"
    else:  # O input que causou o callback não foi um botão
        if args[2] == "bt-product-active":
            return [bt_save], get_table(), no_update, "bt-product-active"
        if args[2] == "bt-select-store":
            return [store_selector_dropdown], None, "bt-select-store"

    return no_update, no_update, no_update, no_update


@app.callback(
    Output("modal-save", "is_open"),
    [Input("bt-save-active", "n_clicks"), Input("product-table", "data")],
    [State("modal-save", "is_open")],
)
def save_active(bt_open, data, is_open):
    if bt_open:
        return not is_open

    df_to_dict = {"0": [], "1": []}
    for row in data:
        if (
            row["Ativo"] == "Nao"
            or row["Ativo"] == "Não"
            or row["Ativo"] == "0"
        ):
            df_to_dict["0"].append(row["Produto"])
        else:
            df_to_dict["1"].append(row["Produto"])

    with open("previsao/ativo.json", "w") as fout:
        json.dump(df_to_dict, fout)  # Salvar o dicionário

    return is_open
