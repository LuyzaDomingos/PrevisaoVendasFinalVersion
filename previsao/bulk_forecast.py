import pandas as pd
import numpy as np

from fbprophet import Prophet

# Criação do dataframe de feriados
mothers = pd.DataFrame({
    'holiday': 'Dia das mães',
    'ds': ['2015-05-10', '2016-05-08', '2017-05-14', '2018-05-13', '2019-05-12', '2020-05-10', '2021-05-09'],
    'lower_window': 0,
    'upper_window': 0
})
fathers = pd.DataFrame({
    'holiday': 'Dia dos pais',
    'ds': ['2015-08-09', '2016-08-14', '2017-08-13', '2018-08-12', '2019-08-11', '2020-08-09', '2021-06-20'],
    'lower_window': 0,
    'upper_window': 0
})
valentines = pd.DataFrame({
    'holiday': 'Dia dos namorados',
    'ds': ['2015-06-12', '2016-06-12', '2017-06-12', '2018-06-12', '2019-06-12', '2020-06-12', '2021-06-12'],
    'lower_window': 0,
    'upper_window': 0
})
christmas = pd.DataFrame({
    'holiday': 'Natal',
    'ds': ['2015-12-25', '2016-12-25', '2017-12-25', '2018-12-25', '2019-12-25', '2020-12-25', '2020-12-25', '2021-12-25'],
    'lower_window': -1, # Incluindo a véspera
    'upper_window': 0
})
bf = pd.DataFrame({
    'holiday': 'Black friday',
    'ds': ['2015-11-27', '2016-11-25', '2017-11-24', '2018-11-25', '2019-11-24', '2020-11-27', '2021-11-25'],
    'lower_window': 0,
    'upper_window': 0
})
childrens = pd.DataFrame({
    'holiday': 'Dia das crianças',
    'ds': ['2015-10-12', '2016-10-12', '2017-10-12', '2018-10-12', '2019-10-12', '2020-10-12', '2021-10-12'],
    'lower_window': 0,
    'upper_window': 0
})
easter = pd.DataFrame({
    'holiday': 'Páscoa',
    'ds': ['2015-04-05', '2016-03-27', '2017-04-16', '2018-04-01', '2019-04-21', '2020-04-12', '2021-04-04'], # Domingo de páscoa
    'lower_window': -2, # Incluindo o fim de semana
    'upper_window': 0
})
new_year = pd.DataFrame({
    'holiday': 'Ano Novo',
    'ds': ['2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01', '2022-01-01'],
    'lower_window': -1, # Adicionar a véspera
    'upper_window': 0
})
carnival = pd.DataFrame({
    'holiday': 'Carnaval',
    'ds': ['2015-02-18', '2016-02-10', '2017-03-01', '2018-02-14', '2019-03-06', '2020-02-26', '2021-02-17'], # Quarta feira de cinzas
    'lower_window': -4, # Incluindo sábado, domingo, segunda e terça
    'upper_window': 0
})

holidays = pd.concat((mothers, fathers, valentines, christmas, bf, childrens, easter, new_year))

def bulk_forecast():
    in_data = pd.read_csv('geral.csv', index_col=0)
    # O prophet tem uma função pra criar uma dataframe futuro
    dummy_data = pd.DataFrame({'ds': pd.to_datetime(['2021-03-16', '2021-03-17']), 'y': [0, 1]})
    ph = Prophet(daily_seasonality=False)
    ph.fit(dummy_data)
    # Criar uma base de dados futura
    future = ph.make_future_dataframe(periods=363, freq='D')
    # Criar as tabelas de saída
    out_forecast = pd.DataFrame(np.zeros((365, len(in_data.columns))), columns=in_data.columns, index=future['ds'])
    out_forecast_lyhat = pd.DataFrame(np.zeros((365, len(in_data.columns))), columns=in_data.columns, index=future['ds'])
    out_forecast_uyhat = pd.DataFrame(np.zeros((365, len(in_data.columns))), columns=in_data.columns, index=future['ds'])
    
    i = 0
    for product in in_data.columns: # Fazer a previsão de tudo
        i += 1
        print("(%d / %d) Gerando previsão de %s" % (i, len(in_data.columns), product))
        # Criar o dataframe no formato do prophet
        prophet_df = pd.DataFrame({'ds': in_data.index, 'y':in_data[product].values})
        prophet = Prophet(daily_seasonality=False, holidays=holidays)
        # Fazer o fit
        prophet.fit(prophet_df)
        # Fazer a previsão
        forecast = prophet.predict(future)
        forecast.index = pd.to_datetime(forecast['ds'])
        # Salvar a previsão nas respectivas tabelas
        out_forecast[product] = forecast['yhat'].apply(lambda x : 0 if x < 0 else round(x))
        out_forecast_uyhat[product] = forecast['yhat_upper'].apply(lambda x : 0 if x < 0 else round(x))
        out_forecast_lyhat[product] = forecast['yhat_lower'].apply(lambda x : 0 if x < 0 else round(x))
    
    print("Previsões encerradas, salvando...")
    out_forecast.to_csv('previsao_geral.csv')
    out_forecast_uyhat.to_csv('previsao_geral_yhat_upper.csv')
    out_forecast_lyhat.to_csv('previsal_geral_yhat_lower.csv')
    print("Tudo certo, encerrando...")
    
if __name__ == '__main__':
    bulk_forecast()

