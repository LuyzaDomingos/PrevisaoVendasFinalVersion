import pandas as pd
import numpy as np

# Salvar tudo
def save_dfs(store_dict):
    for (store, dataframe) in store_dict.items():
        dataframe.to_csv('data/' + store + '.csv')
        
# Criar o grande dataframe
def create_df():
    dfs = []
    for txt in ['2018.txt', '2019.txt', '2020.txt','2021.txt']:
        df = pd.read_csv(txt, delimiter=';', encoding = 'cp1252')
        df.columns = ['COD_FILIAL', 'SIGLA', 'NOME', 'REGIAO', 'COD_PRODUTO', 'PRODUTO', 'COD_GRUPO', 'CLASSIFICACAO', 'QTD_VENDIDA', 'DATA', 'COD_FILIAL_', 'COD_ENTREGA', 'ENTREGA', 'ANO/MES', 'MES', '1', '2', 'CD', '3', '4', 'SUBCATEGORIA', 'FORNECEDOR']
        df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)
        dfs.append(df)
    df = pd.concat(dfs)
    return df
    
def get_dfg(df, general=True, keep_month=True):
    dfg = df.drop(columns=['COD_FILIAL', 'SIGLA', 'REGIAO', 'COD_PRODUTO', 'COD_GRUPO', 'CLASSIFICACAO', 'COD_FILIAL_', 'COD_ENTREGA', 'ENTREGA', 'ANO/MES', '1', '2', 'CD', '3', '4', 'SUBCATEGORIA', 'FORNECEDOR'])
    if general is True:
        dfg.drop(columns=['NOME'], inplace=True)
    if keep_month is False:
        dfg.drop(columns=['MES'], inplace=True)
    
    return dfg

# Pegar as colunas relevantes
def get_data():
    df = create_df()
    dfg = get_dfg(df, general=False, keep_month=False)
    index = pd.date_range(start='2018-01-01', end='2021-04-01', freq='D')
    columns = dfg['PRODUTO'].unique()

    # Criar o dataframe das lojas
    stores = dfg['NOME'].unique()
    stores_dfs = {}

    for store in stores:
        stores_dfs[store] = pd.DataFrame(index=index, columns=columns)
        stores_dfs[store].fillna(value=0, inplace=True)
        
    # Popular os dataframes
    p = s = 0
    num_p = len(columns)
    num_s = len(stores)

    for store in stores: # stores
        s += 1
        print("(%d/%d) %s" % (s, num_s, store))
        for product in columns: # columns
            group = dfg.loc[(dfg['PRODUTO'] == product) & (dfg['NOME'] == store)].groupby(['DATA']).sum()
            p += 1
            print("Store: (%d/%d) %s Product:(%d/%d) %s" % (s, num_s, store, p, num_p, product))
            i = 0
            for row in group.index:
                stores_dfs[store].loc[row][product] = group.iloc[i]['QTD_VENDIDA']
                i += 1
    
    save_dfs(store_dict)
    
if __name__ == '__main__':
    get_data()
