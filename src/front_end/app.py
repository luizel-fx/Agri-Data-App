import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from components.navbar import navbar

from ages.futures.spreads import make_cs_dashboard
from pages.home import make_home

THEME = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=THEME)
app.title = "Agrimensor"

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return make_home()
    if pathname == '/futures/spreads':
        return make_cs_dashboard()


if __name__ == '__main__':
    app.run_server(debug=False)