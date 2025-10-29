import dash
from dash import html
from components.navbar import navbar

def make_home():
    layout = html.Div([
        navbar()
    ])

    return layout