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
        'font-weight': 'normal',
        'margin-left': 0,
        'margin-right': 0,
        'color': '#383838'
        }
    return dbc.NavItem(dbc.NavLink(label, href=href, active="exact"), style = nav_item_style)

def drop_down_menu(label, items_url: dict, icon_path):
    # Estilos para o botão (toggle) do DropdownMenu
    # Removendo 'display: flex' e 'align-items: center' daqui, pois
    # isso será aplicado ao conteúdo do 'label' (o span)
    drop_down_menu_style = {
        "background": "#FFFFFF",
        "color": "#383838",
        "font-size": 20,
        'font-weight': 'normal',
        "padding-right": "0.5rem",
        "display": "flex",
        "align-items": "center",
    }

    # 1. Cria o elemento do ícone
    icon_img = html.Img(
        src=icon_path, 
        width='20px', 
        height='20px', 
        style={'margin-right': '5px'} # Adiciona um pequeno espaço à direita do ícone
    )

    # 2. Combina o ícone e o rótulo em um html.Span.
    # Usamos 'display: flex' aqui para alinhar horizontalmente o ícone e o texto
    dropdown_label_content = html.Span(
        [icon_img, label],
        style={
            'display': 'flex', 
            'align-items': 'center', 
            'line-height': 'normal' # Ajuda na centralização vertical
        } 
    )

    # Cria os itens do menu suspenso (o que cai)
    children = [
        dbc.DropdownMenuItem(
            # Assumindo que 'nav_item' retorna um componente de link (como um 'dbc.NavLink')
            nav_item(item, items_url[item]), 
            class_name='ms-2'
        ) for item in items_url.keys()
    ]

    return dbc.DropdownMenu(
        # Passa o Span (que contém o ícone e o texto) como o rótulo
        label=dropdown_label_content,
        children=children,
        toggle_style=drop_down_menu_style,
        # Você pode querer adicionar um 'className' para estilizar o botão com mais precisão via CSS externo
    )

reports_pages = {
    'Condições das lavouras': '/',
    'Progresso da safra': '/',
    'Oferta e Demanda - USDA': '/',
    'Exportações (EUA)': '/'
}

spot_pages = {
    "Basis": "pages/mercado_fisico/basis",
    "Diferencial de base": "pages/mercado_fisico/basis_diff",
    "Preços relativo": "pages/mercado_fisico/rel_prices"
}

fut_pages = {
    "Spreads": "/",
    "Ratios": "/"
}

home_navbar = html.Div(children=[
    html.Img(src="/assets/home_icon.png", width='20px', height='20px'),
    nav_item("Home", "/")
], style={'display': 'flex', 'align-items': 'center','margin-left': 0, 'margin-right': 0,})

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
                                        #nav_item("Home", "/"),
                                        home_navbar,
                                        drop_down_menu("Relatórios", reports_pages, 'assets/reports_icon.png'),
                                        drop_down_menu("Mercado físico", spot_pages, 'assets/spot_icon.png'),
                                        drop_down_menu("Mercado futuro", fut_pages, 'assets/fut_icon.png')
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