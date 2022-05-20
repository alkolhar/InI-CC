from dash import Dash, html, dcc, Output, callback, Input
import dash_bootstrap_templates as dbt
import dash_bootstrap_components as dbc

# set default theme for plots
from dashboard.functions import elements
from dashboard.pages import explore, analyze_string

dbt.load_figure_template(["bootstrap"])
template_theme = "flatly"
url_theme = dbc.themes.FLATLY

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

app = Dash(__name__, external_stylesheets=[url_theme, dbc_css])

app.title = "Cloud computing: Review analysis"

# TODO: Landing page
body = html.Div([], className="mt-12 container")

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),

        html.Div([elements.navbar, body], id='page-content')
    ]
)


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/explore':
        return explore.layout
    elif pathname == '/analyze-str':
        return analyze_string.layout
    else:
        return app.layout

