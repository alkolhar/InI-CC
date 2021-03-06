import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt
from dash import Dash, html, dcc, Output, callback, Input

from dashboard.pages import explore_cats, analyze_string, analyze_files, explore_products, upload_review, about

dbt.load_figure_template(["bootstrap"])
template_theme = "cyborg"
url_theme = dbc.themes.CYBORG

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

dash_app = Dash(__name__, external_stylesheets=[url_theme, dbc_css], suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1"}])
server = dash_app.server

dash_app.title = "Cloud computing: Review analysis"
dash_app._favicon = "favicon.ico"

dash_app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),

        html.Div([], id='page-content')
    ]
)


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/analyzetext':
        return analyze_string.layout
    elif pathname == '/uploadfile':
        return analyze_files.layout
    elif pathname == '/products':
        return explore_products.layout
    elif pathname == '/uploadreview':
        return upload_review.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/':
        return explore_cats.layout
    else:
        return 404
