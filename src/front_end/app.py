import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# SETTING THEME AND COSMETICS
THEME = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=THEME)
app.title = "Agrimensor"

# NAVIGATION BAR
def navItem(label, href):
    return dbc.NavLink(label, href=href, active="exact")

LOGO = "/assets/logo.png"

def nav_item(label, href):
    """Cria um item de navegação com link para o sidebar."""
    nav_item_style={
        'font-size': 20,
        'display': 'flex',
        'align-items': 'center',
        'margin-left': 16,
        'margin-right': 16,
        'font-weight': 'normal',
        'color': '#383838'
        }
    return dbc.NavItem(dbc.NavLink(label, href=href, active="exact"), style = nav_item_style)

drop_down_menu_style = {
    "background": "#FFFFFF",
    "color": "#383838",
    "font-size": 20,
    'font-weight': 'normal'
} 

navbar = dbc.Navbar(
    dbc.Container(
        [
            # LOGO + 
            html.A(
                dbc.Row(
                    children=[
                        html.Div(
                            [
                                # LOGO
                                html.Img(src=LOGO, height='100px', className='me-2'),
                                #dbc.NavbarBrand("Agrimensor", className='ms-2')

                                # NAVBAR
                                html.Div(
                                    [
                                        nav_item("Home", "/"),
                                        dbc.DropdownMenu(
                                            label = "Relatórios",
                                            children = [
                                                dbc.DropdownMenuItem(
                                                    nav_item("Oferta e Demanda - USDA", "/"), class_name='ms-2'
                                                )
                                            ],
                                            toggle_style = drop_down_menu_style
                                        ),
                                        dbc.DropdownMenu(
                                            label = "Mercado físico",
                                            children = [
                                                dbc.DropdownMenuItem(
                                                    nav_item("Basis", "pages/mercado_fisico/basis"), class_name='ms-2'
                                                ),
                                                dbc.DropdownMenuItem(
                                                    nav_item("Diferencial de base", "pages/mercado_fisico/basis_diff"), class_name='ms-2'
                                                ),
                                                dbc.DropdownMenuItem(
                                                    nav_item("Preços relativo", "pages/mercado_fisico/rel_prices"), class_name='ms-2'
                                                )
                                            ],
                                            toggle_style = drop_down_menu_style
                                        ),
                                        dbc.DropdownMenu(
                                            label = "Mercado futuro",
                                            children = [
                                                dbc.DropdownMenuItem(
                                                    nav_item("Spreads", "/"), class_name='ms-2'
                                                ),
                                                dbc.DropdownMenuItem(
                                                    nav_item("Ratios", "/"), class_name='ms-2'
                                                )
                                                #, dbc.DropdownMenuItem(
                                                #    nav_item("Intra Market-Year SB-Spreads Model", "/"), class_name='ms-2'
                                                #)
                                            ],
                                            toggle_style = drop_down_menu_style
                                        ),
                                    ],
                                    style={"display": 'flex'}
                                )
                            ],
                            style={
                                "display": 'flex',
                                "align-items": "center",
                                "justify-content": "center"
                            }
                        )
                        ]
                    ),
                )
            ]
        )
    )




app.layout = html.Div(children=[navbar])


app.run()