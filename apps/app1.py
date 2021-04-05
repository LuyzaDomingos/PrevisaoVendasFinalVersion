import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
# Dependências do Dash
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash import no_update
# API de previsão de séries temporais
from fbprophet import Prophet
# Funções de plotagem
from util import get_forecast_figure, get_sales_figure

from app import app

# Leitura dos dados, amostragem diária
data_d = pd.read_csv("previsao/geral.csv", index_col=0)
data_d.fillna(value=0, inplace=True)
data_d.index = pd.to_datetime(data_d.index)
data_d = data_d[:'2021-03-12']
# Amostragem semanal
data_w = pd.read_csv("previsao/WGeral.csv", index_col=0)
data_w.fillna(value=0, inplace=True)
data_w.index = pd.to_datetime(data_w.index)
data_w = data_w[:'2021-03-12']
# Amostragem mensal
data_m = pd.read_csv("previsao/MonGeral.csv", index_col=0)
data_m.fillna(value=0, inplace=True)
data_m.index = pd.to_datetime(data_m.index)
data_m = data_m[:'2021-03-12']
# Criação do dataframe de feriados
mothers = pd.DataFrame({
    'holiday': 'Dia das mães',
    'ds': ['2015-05-10', '2016-05-08', '2017-05-14', '2018-05-13', '2019-05-12'],
    'lower_window': -7,
    'upper_window': 0
})
fathers = pd.DataFrame({
    'holiday': 'Dia dos pais',
    'ds': ['2015-08-09', '2016-08-14', '2017-08-13', '2018-08-12', '2019-08-11'],
    'lower_window': -7,
    'upper_window': 0
})
valentines = pd.DataFrame({
    'holiday': 'Dia dos namorados',
    'ds': ['2015-06-12', '2016-06-12', '2017-06-12', '2018-06-12', '2018-06-12'],
    'lower_window': -7,
    'upper_window': 0
})
christmas = pd.DataFrame({
    'holiday': 'Natal',
    'ds': ['2015-12-25', '2016-12-25', '2017-12-25', '2018-12-25', '2019-12-25'],
    'lower_window': -8, # Incluindo a véspera
    'upper_window': 0
})
bf = pd.DataFrame({
    'holiday': 'Black friday',
    'ds': ['2015-11-27', '2016-11-25', '2017-11-24', '2018-11-25', '2019-11-24'],
    'lower_window': -7,
    'upper_window': 0
})
childrens = pd.DataFrame({
    'holiday': 'Dia das crianças',
    'ds': ['2015-10-12', '2016-10-12', '2017-10-12', '2018-10-12', '2019-10-12'],
    'lower_window': -7,
    'upper_window': 0
})
easter = pd.DataFrame({
    'holiday': 'Páscoa',
    'ds': ['2015-04-05', '2016-03-27', '2017-04-16', '2018-04-01', '2019-04-21'], # Domingo de páscoa
    'lower_window': -7,
    'upper_window': 0
})
new_year = pd.DataFrame({
    'holiday': 'Ano Novo',
    'ds': ['2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01'],
    'lower_window': -8, # Adicionar a véspera
    'upper_window': 0
})
carnival = pd.DataFrame({
    'holiday': 'Carnaval',
    'ds': ['2015-02-18', '2016-02-10', '2017-03-01', '2018-02-14', '2019-03-06'], # Quarta feira de cinzas
    'lower_window': -7, # Adicionar a véspera
    'upper_window': 0
})

holidays = pd.concat((mothers, fathers, valentines, christmas, bf, childrens, easter, new_year))
# Dicionário de fornecedores
suppliers_dict = json.load(open('previsao/fornecedores2.json'))
# Dicionário de frequências
freq_dict = {
    'Diário': 'D',
    'Semanal': 'W-MON',
    'Mensal': 'M'
}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Avenir:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

heroku = True
products = data_d.columns
if heroku is True:
    products = ['CONDICIONADOR DE AR TIPO SPLIT FIT CCSF9-R4', 'REFRIGERADOR ROC 31 BR']
    suppliers_dict = {"ESMALTEC": ["REFRIGERADOR ROC 31 BR"], "VIVO": ["CHIP VIVO 4G 128K P19 HRS PRE"]}
    
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Previsão de vendas", className="header-title"),
                html.P(children="Visualização e previsão de séries temporais referentes à vendas de produtos", className="header-description"),
                html.Button("Baixe a previsão (.csv)", id="bt-download", className="bt"),
                Download(id="download")
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Fornecedor", className="menu-title"),
                        dcc.Dropdown(
                            id="supplier-filter",
                            options=[{"label": key, "value": key} for key in list(suppliers_dict.keys())],
                            value="ESMALTEC",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": product, "value": product}
                                for product in suppliers_dict["ESMALTEC"]
                            ],
                            value="REFRIGERADOR ROC 31 BR",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Frequência", className="menu-title"),
                        dcc.Dropdown(
                            id="frequency-selector",
                            options=[{"label": key, "value": value} for key, value in freq_dict.items()],
                            value="D",
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
                            min_date_allowed=data_d.index.min().date(),
                            max_date_allowed=data_d.index.max().date(),
                            start_date=data_d.index.min().date(),
                            end_date=data_d.index.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
#        html.Div(
#            children=[
#                html.Div(
#                    children=dcc.Graph(
#                        id="sales-chart-cumsum", config={"displayModeBar": False},
#                    ),
#                    className="card",
#                ),
#            ],
#            className="wrapper",
#        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales-chart-period", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=dcc.Graph(
                id="forecast-chart", config={"displayModeBar": False},
            ),
            className="wrapperSecond",
        ),
    ]
)

# Callback do botão de baixar previsão
@app.callback(
    Output("download", "data"),
    [Input("bt-download", "n_clicks"), Input("product-filter", "value"), Input("frequency-selector", "value")]
)
def download_forecast(n_clicks, product, frequency):
    if n_clicks is None:
        return no_update
        
    path = "previsao/forecasts/" + frequency + "/" + product.replace(" ", "_").replace("/", "_") + ".csv"
    try:
        forecast = pd.read_csv(path)
        forecast.index = pd.to_datetime(forecast['ds'])
        return send_data_frame(forecast.to_csv, filename="Previsao_" + product.replace(" ", "_").replace("/", "_") + ".csv")
    except:
        return html.Div("Um erro ocorreu ao tentar obter a previsão!")
    

# Callback da seleção de fornecedor
@app.callback(
    [Output("product-filter", "options"), Output("product-filter", "value")],
    [Input("supplier-filter", "value")]
)
def update_products(supplier):
    return [{"label": product, "value": product} for product in suppliers_dict[supplier]], suppliers_dict[supplier][0]

# Callback da seleção de produto, frequência, e data
@app.callback(
# Lembrete: Se tiver mais de uma chamada de Output(...) colocar em uma lista as multiplas chamadas
    #[Output("sales-chart-cumsum", "figure"), Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")],
    [Output("sales-chart-period", "figure"), Output("forecast-chart", "figure")],
    [Input("product-filter", "value"), Input("frequency-selector", "value"), Input("date-range", "start_date"), Input("date-range", "end_date")]
)
def update_charts(product, frequency, start_date, end_date):
    if frequency == 'D':
        mask = (
        (data_d.index >= start_date)
        & (data_d.index <= end_date)
        )
        filtered_data = data_d.loc[mask, :]
    elif frequency == 'W-MON':
        mask = (
        (data_w.index >= start_date)
        & (data_w.index <= end_date)
        )
        filtered_data = data_w.loc[mask, :]
    else: # frequency == 'M'
        mask = (
        (data_m.index >= start_date)
        & (data_m.index <= end_date)
        )
        filtered_data = data_m.loc[mask, :]
        
    filtered_data = filtered_data.resample(frequency).sum()
    
    sales_period_chart_figure = get_sales_figure(filtered_data, product)
    forecast_chart_figure = get_forecast_figure(filtered_data, product, '2021-01-01', frequency)
    
    return sales_period_chart_figure, forecast_chart_figure
