import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3,app4

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
        ],className = "header"),

        html.A(
            children=[
                html.Img(src=app.get_asset_url('serie.png'),style = {'width':'100px', 'height':'100px','display':'table'}),
                 html.P("Previsão por Produtos",className='secondlink'),

            ],href='/apps/app1',className="column",
        ),
        html.A(
            children=[
                html.Img(src=app.get_asset_url('previsao.png'),style = {'width':'100px', 'height':'100px','display':'table'}),
                html.P("Previsão por Categoria",className='secondlink'),

            ],href='/apps/app2',className="column",
        ),
        html.A(
            children=[
                html.Img(src=app.get_asset_url('serie.png'),style = {'width':'100px', 'height':'100px','display':'table'}),
                html.P("Panorama por Categoria",className='secondlink'),

            ],href='/apps/app3',className="column",
        ),
        html.A(
            children=[
                html.Img(src=app.get_asset_url('venda.png'),style = {'width':'100px', 'height':'100px','display':'table'}),
                html.P("Painel de Vendas",className='secondlink')

            ],href='/apps/app4',className="column",
        ),
    
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    elif pathname == '/apps/app4':
        return app4.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)

