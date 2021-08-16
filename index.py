import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3, app4

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(children =[
    html.Div(
        children=[
            html.P(children="📈", className="header-emoji"),
            html.H1(children="Previsão de Vendas", className="header-title"),
            html.P(children="Visualização e previsão de séries temporais referentes à vendas de produtos", className="header-description"),
            # html.Img(src=app.get_asset_url('previsao.png'),className = 'link'),
            # dcc.Link('Previsão por Produtos', href='/apps/app1',className='link'),
            # dcc.Link('Previsão por Categorias', href='/apps/app2',className='link'),
            # dcc.Link('Panorama de Categoria', href='/apps/app3', className='link'),
            # dcc.Link('Painel de Vendas', href='/apps/app4', className='link')
        ],className = "header", style = {'height':'200px'}),
        html.Div(
            children=[
        html.A(
            children=[
                html.Img(src=app.get_asset_url('serie.png'), style = {'width':'100px', 'height':'100px'}),
                html.P("Previsão por Produtos", className='secondlink'),
            ],href='/apps/app1',className="column",
        ),
        html.A(
            children=[
                html.Img(src=app.get_asset_url('previsao.png'), style = {'width':'100px', 'height':'100px'}),
                html.P("Previsão por Categoria", className='secondlink'),
            ],href='/apps/app2',className="column",
        ),
        #html.A(
            #children=[
                #html.Img(src=app.get_asset_url('serie.png'), style = {'width':'100px', 'height':'100px'}),
                #html.P("Panorama por Categoria",className='secondlink', style = {'text-decoration':'none'}),
            #],href='/apps/app3',className="column",
        #),
        html.A(
            children=[
                html.Img(src=app.get_asset_url('venda.png'), style = {'width':'100px', 'height':'100px'}),
                html.P("Painel de Vendas", className='secondlink') # style = {'color': 'gray'}
            ], href='/apps/app4',className="column",
        ),
        ], style = {'width':'100%', 'height':'100%','display':'flex', 'justify-content': 'space-evenly', 'padding-top': '50px'}),
    
])

categories_paths = ['/apps/' + category.replace(' ', '_') for category in ['ELETRO LINHA BRANCA', 'ELETRO TV E SOM',
       'ELETRO TELEFONIA CELULAR', 'ELETRO INFORMATICA', 'MOVEIS COLCHAO',
       'ELETRO PORTATEIS', 'MOVEIS MADEIRA', 'ELETRO UTILIDADE DO LAR',
       'MOVEIS ACO, TUBO E PLASTICO', 'ELETRO BIC.,BRINQ. E CARRO DE',
       'MOVEIS ESTOFADOS', 'ELETRO AUTO RADIO', 'ELETRO ELETRO RELOGIO',
       'ELETRO TELEFONES E ACESSORIOS', '0', 'INFORMATICA',
       'ELETRO MOTOCICLETAS', 'UTILIDADES DOMESTICAS', 'MOVEIS',
       'ELETROPORTATEIS', 'ELETRODOMESTICOS', 'COLCHAO',
       'AR E VENTILACAO', 'BELEZA E SAUDE', 'AUDIO E SOM', 'BRINQUEDOS',
       'CELULAR', 'MÓVEIS', 'AUTOMOTIVO', 'TV E VIDEO',
       'ESPORTE E FITNESS', 'BEBE', 'AR E VENTILAÇÃO', 'RELOGIO', 'GAMES',
       'GAME', '1000', 'ESPORTE E LAZER', 'GARRAFA TERMICA',
       'ATIVO IMOBILIZADO']]

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.get_layout()
    elif pathname == '/apps/app4':
        return app4.layout
    # Pathname usado para dar o panorama da categoria correspondente
    elif pathname in categories_paths:
       return app3.get_layout(pathname[6:].replace('_', ' '))
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
    # app.run_server(host='127.0.0.1', debug=True)

