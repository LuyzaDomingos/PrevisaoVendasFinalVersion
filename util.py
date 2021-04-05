import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from fbprophet import Prophet

def get_forecast_figure(filtered_data, product, split_date, freq='D'):
    size_train = len(filtered_data[:split_date])
    size_test = len(filtered_data[split_date:])
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
        if heroku is False:
            forecast.to_csv(path)
        
    fig = px.line(range_x=['2018-01-01', '2021-03-12'],
                    range_y=[0, max(filtered_data[product] * 1.1)],
                    labels={'y': 'Quantidade Vendida', 'x': 'Período'},
                    title='Projeção de vendas')

    fig.add_trace(go.Scatter(x=filtered_data[size_train:].index, y=filtered_data[product][size_train:],
                        mode='markers',
                        name='Vendas observadas',
                        showlegend=False,
                        line={'color': '#045dd1'}))
       
    #fig.add_trace(go.Bar(x=data[split_date:].index, y=data[product][split_date:],
    #                    name='Vendas observadas',
    #                    showlegend=False))
                        
    fig.add_trace(go.Scatter(x=filtered_data[:size_train].index, y=filtered_data[product][:size_train],
                        mode='lines',
                        name='Vendas observadas',
                        line={'color': '#045dd1'}))
                        
    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat'][size_train:],
                        mode='lines',
                        name='Vendas projetadas',
                        line={'color': '#d10b04'}))

    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat_lower'][size_train:],
                        #mode='none',
                        name='Limite inferior',
                        showlegend=False,
                        line_color='rgba(192, 43, 29, 0.2)'))
                        
    fig.add_trace(go.Scatter(x=forecast[size_train:].index, y=forecast['yhat_upper'][size_train:],
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
                  y1=999,
                  line={'color': '#c4c7cc'})
                  
    fig.layout.xaxis.linecolor='rgba(0, 0, 0, 1)'
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'

    return fig
    
def get_sales_figure(filtered_data, product):
    # Criar uma figura com eixos secundários
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(title_text="Vendas observadas", xaxis_range=['2018-01-01', '2021-03-12'])
    
    # Adicionar as linhas
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product].cumsum(), name="Vendas acumuladas", line={'color': '#045dd1'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[product], name="Novas vendas", line={'color': 'rgba(101, 156, 0, 0.8)'}), secondary_y=True)

    # Nome dos eixos
    fig.update_yaxes(title_text="Vendas acumuladas", secondary_y=False)
    fig.update_yaxes(title_text="Novas Vendas", secondary_y=True)

    # Linha y = 0
    fig.add_shape(type='line', x0='2018-01-01', y0=0, x1='2021-03-12', y1=0, line={'color': 'rgba(0, 0, 0, 1)'})
    # Cores do gráfico
    fig.layout.xaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.yaxis.gridcolor='rgba(189, 189, 189, 0.5)'
    fig.layout.plot_bgcolor='rgba(255, 255, 255, 1)'
    
    return fig
