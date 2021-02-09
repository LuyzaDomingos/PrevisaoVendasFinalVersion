import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

data = pd.read_csv("previsao/dfw.csv")
forecast = pd.read_csv("previsao/forecast.csv")

data.index = pd.to_datetime(data['Unnamed: 0'])
data.drop(columns=['Unnamed: 0'], inplace=True)

forecast.index = pd.to_datetime(forecast['ds'])
forecast.drop(columns=['ds'], inplace=True)
              
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Avenir:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Previsão de vendas"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Previsão de vendas", className="header-title"
                ),
                html.P(
                    children="Visualização da série temporal de Smartphones"
                    " da família Samsung Galaxy J vendidos"
                    " entre 2015 e 2019",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": product, "value": product}
                                for product in data.columns
                            ],
                            value="SMARTPHONE SAMSUNG GAL J1 ACE J110L DB BCO",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Intervalo de datas",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.index.min().date(),
                            max_date_allowed=data.index.max().date(),
                            start_date=data.index.min().date(),
                            end_date=data.index.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
#        html.Div(
#            children=dcc.Graph(
#                id="forecast-chart",
#                config={"displayModeBar": False},
#                figure={
#                    "data": [
#                        {
#                            "x": data.index,
#                            "y": [forecast['yhat'], data['j2_prime_successor']],
#                            "type": "lines",
#                        },
#                    ],
#                    "layout": {
#                        "title": {
#                            "text": "Previsão de Vendas (J2 Prime)",
#                            "x": 0.05,
#                            "xanchor": "left",
#                        },
#                        "xaxis": {"fixedrange": True},
#                        "yaxis": {"fixedrange": True},
#                        "colorway": ["#d10b04", "#045dd1"],
#                    },
#                },
#            ),
#            className="wrapper",
#        ),
    ]
)

@app.callback(
# Lembrete: Se tiver mais de uma chamada de Output(...) colocar em uma lista as multiplas chamadas
    Output("sales-chart", "figure"),
    [
        Input("product-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

def update_charts(product, start_date, end_date):
    mask = (
        (data.index >= start_date)
        & (data.index <= end_date)
    )
    filtered_data = data.loc[mask, :]
    sales_chart_figure = {
        "data": [
            {
                "x": filtered_data.index,
                "y": filtered_data[product],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Quantidade vendida",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#045dd1"],
        },
    }

    return sales_chart_figure

    
if __name__ == "__main__":
    app.run_server(debug=True)
