import dash
import dash_auth
# Usuário e senha para acessar o dashboard
password_dict = {'armazem': 'pb'}

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Previsão de vendas"
auth = dash_auth.BasicAuth(app, password_dict)
server = app.server
