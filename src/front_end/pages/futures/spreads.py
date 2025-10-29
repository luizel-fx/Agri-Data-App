import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from components.navbar import navbar

from components.navbar import navbar

# =
# = INPUTS
# =

asset = html.Div(children=[
    dcc.Markdown("Ativo"),
    dcc.Dropdown(
        id = 'asset',
        options = [
            {'label': "Soja CBOT", 'value': 'ZS'},
            {'label': "Milho B3", 'value': 'CCM'},
            {'label': "Boi Gordo B3", 'value': 'BGI'}
        ],
        value = 'ZS'
    )
    ]
    )

short_exp = html.Div([
    dcc.Markdown("Contrato curto"),
    dcc.Input(
        id='short_exp',
        type='text',
        placeholder='Ex: X2026'
    )
    ]
)

long_exp = html.Div([
    dcc.Markdown("Contrato longo"),
    dcc.Input(
        id='long_exp',
        type='text',
        placeholder='Ex: N2026',
    )
    ]
)

input_div = html.Div(
    children=[
        asset, short_exp, long_exp
    ],
    style={
        'display': 'flex'
    }
)

def make_cs_dashboard():
    layout = html.Div(
        [
        navbar(),
        input_div
        ]
        )

    return layout