import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from fbprophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from random import randint

import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable

from app import app

from random import randint

legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)

# Carregar as previsões
yhat_df = pd.read_csv('previsao/previsao_geral.csv', index_col=0)
yhat_lower_df = pd.read_csv('previsao/previsal_geral_yhat_lower.csv', index_col=0) # O nome do arquivo está correto, porém incorretamente escrito
yhat_upper_df = pd.read_csv('previsao/previsao_geral_yhat_upper.csv', index_col=0)
# Converter os índices para datetime
yhat_df.index = pd.to_datetime(yhat_df.index)
yhat_lower_df.index = pd.to_datetime(yhat_lower_df.index)
yhat_upper_df.index = pd.to_datetime(yhat_upper_df.index)
# Dicionário de previsões
forecast_dict = {
    'D': [yhat_df.resample('D').sum(), yhat_lower_df.resample('D').sum(), yhat_upper_df.resample('D').sum()],
    'W-MON': [yhat_df.resample('W-MON').sum(), yhat_lower_df.resample('W-MON').sum(), yhat_upper_df.resample('W-MON').sum()],
    'M': [yhat_df.resample('M').sum(), yhat_lower_df.resample('M').sum(), yhat_upper_df.resample('M').sum()]
}

def heroku():
    return False

def get_forecast_figure(filtered_data, product, split_date, freq='D'):
    size_train = len(filtered_data[:split_date])
    size_test = len(filtered_data[split_date:])
    '''
    path = "previsao/forecasts/" + freq + "/" + product.replace(" ", "_").replace("/", "_") + ".csv"
    # Uma espécie de cache para não repetir a computação do modelo toda vez que selecionar um produto
    try:
        forecast = pd.read_csv(path)
        forecast.index = pd.to_datetime(forecast['ds'])
    except:
        # Criação do dataframe para o Prophet
        prophet_df = pd.DataFrame({'ds': filtered_data.index, 'y':filtered_data[product].values})
        
        prophet = Prophet(daily_seasonality=False, holidays=holidays)
        prophet.fit(prophet_df[:size_train])

        future = prophet.make_future_dataframe(periods=size_test, freq=freq)
        forecast = prophet.predict(future)
        forecast.index = pd.to_datetime(forecast['ds'])
        if heroku() is False:
            forecast.to_csv(path)
    
    forecast['yhat'] = forecast['yhat'].apply(lambda x : 0 if x < 0 else round(x))
    forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x : 0 if x < 0 else round(x))
    forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x : 0 if x < 0 else round(x))
    '''
    fig = px.line(range_x=['2018-01-01', '2022-01-01'],
                    range_y=[0, max(filtered_data[product] * 1.1)],
                    labels={'y': 'Quantidade Vendida', 'x': 'Período'},
                    title='Projeção de vendas')
    '''
    fig.add_trace(go.Scatter(x=filtered_data[size_train:].index, y=filtered_data[product][size_train:],
                        mode='markers',
                        name='Vendas observadas',
                        showlegend=False,
                        line={'color': '#045dd1'}))
    '''
    fig.add_trace(go.Scatter(x=filtered_data[:size_train].index, y=filtered_data[product][:size_train],
                        mode='lines',
                        name='Vendas observadas',
                        line={'color': '#045dd1'}))
                        
    fig.add_trace(go.Scatter(x=forecast_dict[freq][0].index, y=forecast_dict[freq][0][product],
                        mode='lines',
                        name='Vendas projetadas',
                        line={'color': '#d10b04'}))

    fig.add_trace(go.Scatter(x=forecast_dict[freq][0].index, y=forecast_dict[freq][1][product],
                        #mode='none',
                        name='Limite inferior',
                        showlegend=False,
                        line_color='rgba(192, 43, 29, 0.2)'))
                        
    fig.add_trace(go.Scatter(x=forecast_dict[freq][0].index, y=forecast_dict[freq][2][product],
                        #mode='none',
                        fill='tonexty',
                        fillcolor='rgba(192, 43, 29, 0.2)',
                        name='Limite superior',
                        showlegend=False,
                        line_color='rgba(192, 43, 29, 0.2)'))
                        
    fig.add_shape(type='line',
                  x0=split_date,
                  y0=0,
                  x1=split_date,
                  y1=max(filtered_data[product] * 1.1),
                  line={'color': '#c4c7cc'})
                  
    fig.layout.xaxis.linecolor='rgba(0, 0, 0, 1)'
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'
    fig.update_layout(legend=legend)
            
    #return fig, forecast
    return fig, None
    
def get_sales_figure(filtered_data, product):
    # Criar uma figura com eixos secundários
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(title_text="Vendas observadas", xaxis_range=['2018-01-01', '2021-03-12'])
    fig.update_layout(legend=legend)
        
    # Adicionar as linhas
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product].cumsum(), name="Vendas acumuladas", line={'color': '#045dd1'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product], name="Vendas no período", line={'color': 'rgba(101, 156, 0, 0.8)'}), secondary_y=True)

    # Nome dos eixos
    fig.update_yaxes(title_text="Vendas acumuladas", secondary_y=False)
    fig.update_yaxes(title_text="Vendas no período", secondary_y=True)

    # Linha y = 0
    fig.add_shape(type='line', x0='2018-01-01', y0=0, x1='2021-03-12', y1=0, line={'color': 'rgba(0, 0, 0, 1)'})
    # Cores do gráfico
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'
    
    return fig

def get_indicators_figure(filtered_data, forecast, product, split_date):
    size_train = len(filtered_data[:split_date])
    size_test = len(filtered_data[split_date:])

    mse = mean_squared_error(filtered_data[product][size_train:], forecast['yhat'][size_train:len(filtered_data)])
    mad = mean_absolute_error(filtered_data[product][size_train:], forecast['yhat'][size_train:len(filtered_data)])

    fig = go.Figure()
    fig.update_layout(height=120, margin=dict(l=40, r=40, t=40, b=8))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = mse,
        title = {"text": "Erro médio quadrático"},
        #delta = {'reference': 400, 'relative': True},
        domain = {'row': 0, 'column': 0}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = mad,
        #title = {"text": "Erro médio absoluto<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
        title = {'text': 'Erro médio absoluto'},
        #delta = {'reference': 400, 'relative': True},
        domain = {'row': 0, 'column': 1}))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Speed"},
            'mode' : "number+delta+gauge",
            'delta' : {'reference': 90}}]
                             }})

    return fig

def get_list(facts, sort_by='Venda prevista', ascending=False, month=3, year=2021, sales_panel=False, items=None):
    filtered_facts = facts.loc[(facts['Mes'] == month) & (facts['Ano'] == year)]
    filtered_facts = filtered_facts.sort_values(by=sort_by, ascending=ascending)
    child = []

    fig = go.Figure()
    fig.update_layout(height=80, margin=dict(l=40, r=40, t=40, b=8), plot_bgcolor='rgb(255,0,0)')
    
    titles = ["Vendas no período", "Valor das vendas"]
    n_cols = 2
    if sales_panel is False:
        titles.insert(1, "Estoque atual")
        titles[0] = "Venda prevista"
        n_cols = 3
    
    # Soma de todas as vendas previstas
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = filtered_facts['Venda prevista'].sum(),
        title = {"text": titles[0]},
        delta = {'reference': filtered_facts['Venda anterior'].sum(), 'relative': True, 'position': 'right'},
        domain = {'row': 0, 'column': 0}))
    
    if sales_panel is False:
        # Soma de todos os estoques
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = filtered_facts['Estoque atual'].sum(),
            title = {"text": titles[1]},
            delta = {'reference': filtered_facts['Estoque anterior'].sum(), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 1}))
        # Soma de todos os valores
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = filtered_facts['Valor venda'].sum(),
            title = {"text": titles[2]},
            number = {'prefix': "R$"},
            delta = {'reference': filtered_facts['Valor anterior'].sum(), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 2}))
    else:
        # Soma de todos os valores
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = filtered_facts['Valor venda'].sum(),
            title = {"text": titles[1]},
            number = {'prefix': "R$"},
            delta = {'reference': filtered_facts['Valor anterior'].sum(), 'relative': True, 'position': 'right'},
            domain = {'row': 0, 'column': 1}))
            
    grid = {'rows': 1, 'columns': n_cols, 'pattern': "independent"}
    template = {'data' : {'indicator': [{'title': {'text': "Speed"}, 'mode' : "number+delta+gauge", 'delta' : {'reference': 90}}]}}
    fig.update_layout(grid=grid, template=template)

    child.append(html.Div(children=[dcc.Graph(id="sales-chart-period-header", config={"displayModeBar": False}, figure=fig)], className="card small-margin"))

    if sales_panel is True:
        itr = items
    else:
        itr = filtered_facts['Categoria'].unique()
        
    for category in itr:
        fig = go.Figure()
        fig.update_layout(height=80, margin=dict(l=40, r=40, t=8, b=8), plot_bgcolor='#333333')
        if sales_panel is False:
            # Indicador de vendas previstas
            fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = filtered_facts.loc[filtered_facts['Categoria']==category, 'Venda prevista'].values[0],
                title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
                delta = {'reference': filtered_facts.loc[filtered_facts['Categoria']==category, 'Venda anterior'].values[0], 'relative': True, 'position': 'right'},
                domain = {'row': 0, 'column': 0}))
            # Indicador de estoque
            fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = filtered_facts.loc[filtered_facts['Categoria']==category, 'Estoque atual'].values[0],
                title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
                delta = {'reference': filtered_facts.loc[filtered_facts['Categoria']==category, 'Estoque anterior'].values[0], 'relative': True, 'position': 'right'},
                domain = {'row': 0, 'column': 1}))
            # Indicador de valor
            fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = filtered_facts.loc[filtered_facts['Categoria']==category, 'Valor venda'].values[0],
                title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
                number = {'prefix': "R$"},
                delta = {'reference': filtered_facts.loc[filtered_facts['Categoria']==category, 'Valor anterior'].values[0], 'relative': True, 'position': 'right'},
                domain = {'row': 0, 'column': 2}))
        else:
            # Indicador de vendas
            fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = randint(0, 999),
                title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
                delta = {'reference': randint(0, 999), 'relative': True, 'position': 'right'},
                domain = {'row': 0, 'column': 0}))
            # Indicador de valor
            fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = randint(0, 999999),
                title = {"text": "<span style='font-size:0.01em;color:gray'></span>"},
                number = {'prefix': "R$"},
                delta = {'reference': randint(0, 999999), 'relative': True, 'position': 'right'},
                domain = {'row': 0, 'column': 1}))
                
        fig.update_layout(grid=grid, template=template)

        if sales_panel is False:
            child.append(html.Div(children=[
                dcc.Link("    " + category, href='index', className='link white-bg'),
                html.Div(children=[
                    html.Img(src=app.get_asset_url('categorias/' + category + '.png')),
                    dcc.Graph(id="sales-chart-period-" + category, config={"displayModeBar": False}, figure=fig),
                    html.Img(src=app.get_asset_url('graficos.png'), className='yellow-bg'),
                    html.Img(src=app.get_asset_url('relatorio.png'), className='yellow-bg')],
                    className='class-header')
                ], className="card small-margin"))
        else:
            child.append(html.Div(children=[
                dcc.Link("    " + category, href='index', className='link white-bg'),
                html.Div(children=[
                    dcc.Graph(id="sales-chart-period-" + category, config={"displayModeBar": False}, figure=fig),
                    html.Img(src=app.get_asset_url('relatorio.png'), className='yellow-bg')],
                    className='class-header')
                ], className="card small-margin"))

    return child

def get_top_list(data, category_products, month=3, year=2021, top=5):
    filtered_data = data[category_products]
    filtered_data.index = pd.to_datetime(filtered_data.index)
    filtered_data = filtered_data.loc[(data.index.month == month) & (data.index.year == year)]

    num = top
    if(len(category_products) < num): # Em algumas categorias o número de produtos pertencentes é menor que 5
        top_series = filtered_data.sum().sort_values(ascending=False)
        num = len(category_products)
    else:
        top_series = filtered_data.sum().sort_values(ascending=False)[:num]
        
    return  pd.DataFrame({'Produto': top_series.index, 'Qtd. vendida': top_series.values}, index=range(1, num+1))
    
def draw_top_list(data, category_products, month=3, year=2021, top=5):
    top_df = get_top_list(data, category_products, month, year, top)
    
    return DataTable(id='top-table',
                    columns=[{'name': column, 'id': column} for column in top_df.columns],
                    data=top_df.to_dict('records'),
                    style_as_list_view=True,
                    style_data={
                        'textAlign': 'center',
                        'whiteSpace': 'normal',
                        'width': '100%',
                        'overflowY': 'auto',
                        'fontFamily': 'Avenir',
                        'fontSize': '16px',
                        'padding': '12px'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'textAlign': 'center',
                        'fontFamily': 'Avenir',
                        'fontSize': '16px',
                        'padding': '12px'
                    },
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }])
    
