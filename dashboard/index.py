from dash import Dash, html, dcc, Output, callback, Input
import dash_bootstrap_templates as dbt
import dash_bootstrap_components as dbc

# set default theme for plots
from dashboard.layout import elements
from dashboard.pages import home, p_analyze

dbt.load_figure_template(["bootstrap"])
template_theme_light = "flatly"
url_theme_light = dbc.themes.FLATLY

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

app = Dash(__name__, external_stylesheets=[url_theme_light, dbc_css])

app.title = "Cloud computing: Review analysis"

# TODO: Landing page
body = html.Div([])

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),

        html.Div([elements.navbar, body], id='page-content')
    ]
)


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        return home.layout
    elif pathname == '/page2':
        return p_analyze.layout
    else:
        return app.layout

