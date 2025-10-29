import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

LOGO = "/assets/logo.png"

# ======================================== #
# = DEFINING THE NAVBAR AND ITS ELEMENTS = #
# ======================================== # 

def nav_item(label, href):
    nav_item_style={
        'font-size': 20,
        'display': 'flex',
        'align-items': 'center',
        'font-weight': 'normal',
        'margin-left': 0,
        'margin-right': 0,
        'background-color': '#ffffff',
        'color': '#383838'
        }
    return dbc.NavItem(dbc.NavLink(label, href=href, active="exact"), style = nav_item_style)

def drop_down_menu(label, items_url: dict, icon_path):
    drop_down_menu_style = {
        "color": "#383838",
        "font-size": 20,
        'font-weight': 'normal',
        "padding-right": "0.5rem",
        "display": "flex",
        "align-items": "center",
        'background-color': '#ffffff'
    }
    icon_img = html.Img(
        src=icon_path, 
        width='20px', 
        height='20px', 
        style={'margin-right': '5px'} # Adiciona um pequeno espaço à direita do ícone
    )

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

# ============ #
# = NAGATION = #
# ============ #

REPORTS_PAGES = {
    'Condições das lavouras': '/reports/condicoes',
    'Progresso da safra': '/reports/progresso',
    'Oferta e Demanda - USDA': '/reports/usda',
    'Exportações (EUA)': '/reports/exportacoes'
}

SPOT_PAGES = {
    "Basis": "/mercado-fisico/basis",
    "Diferencial de base": "/mercado-fisico/basis-diff",
    "Preços relativo": "/mercado-fisico/rel-prices"
}

FUT_PAGES = {
    "Spreads": "/futures/spreads",
    "Ratios": "/futures/ratios"
}

def home_link():
    return html.Div(children=[
        html.Img(src="/assets/home_icon.png", width='20px', height='20px'),
        nav_item("Home", "/")
    ], style={'display': 'flex', 'align-items': 'center','margin-left': 0, 'margin-right': 0,})

def navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                # LOGO + 
                html.A(
                    dbc.Row(
                        children=[
                            html.Div(
                                    children=[
                                        # LOGO
                                        html.Img(src=LOGO, height='100px', className='me-2'),
                                        #dbc.NavbarBrand("Agrimensor", className='ms-2')

                                        # NAVBAR
                                        html.Div(
                                            [
                                                #nav_item("Home", "/"),
                                                home_link(),
                                                drop_down_menu("Relatórios", REPORTS_PAGES, '/assets/reports_icon.png'),
                                                drop_down_menu("Mercado físico", SPOT_PAGES, '/assets/spot_icon.png'),
                                                drop_down_menu("Mercado futuro", FUT_PAGES, '/assets/fut_icon.png')
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
                        )
                    )
                ]
            )
        )