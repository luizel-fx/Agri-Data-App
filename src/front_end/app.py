import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from components.navbar import navbar

# SETTING THEME AND COSMETICS
THEME = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=THEME)
app.title = "Agrimensor"

LOGO = "/assets/logo.png"

app.layout = html.Div(children=[navbar()])


app.run()