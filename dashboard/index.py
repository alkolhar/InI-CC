from dash import Dash, html, dcc, Output, callback, Input
import dash_bootstrap_templates as dbt
import dash_bootstrap_components as dbc

# set default theme for plots
from dashboard.functions import elements
from dashboard.pages import explore, analyze_string, analyze_files

dbt.load_figure_template(["bootstrap"])
template_theme = "flatly"
url_theme = dbc.themes.FLATLY

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

app = Dash(__name__, external_stylesheets=[url_theme, dbc_css], suppress_callback_exceptions=True)

app.title = "Cloud computing: Review analysis"

# Landing page
files_card = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Analyse files")
        ),
        dbc.CardBody(
            html.P("This is the place to analyse review files")
        ),
        dbc.CardFooter(
            dbc.Button("Analyze files", href="/analyze-file", color="primary")
        )
    ]
)
string_card = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Analyse texts")
        ),
        dbc.CardBody(
            html.P("This is the place to analyse your own texts")
        ),
        dbc.CardFooter(
            dbc.Button("Analyze texts", href="/analyze-str", color="primary")
        )
    ]
)
explore_card = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Explore out database")
        ),
        dbc.CardBody(
            html.P("This is the place to explore already analysed data")
        ),
        dbc.CardFooter(
            dbc.Button("Explore data", href="/explore", color="primary")
        )
    ]
)

# TODO: Landing page
body = html.Div([
    dbc.Row(
        [
            dbc.Col(files_card),
            dbc.Col(string_card),
            dbc.Col(explore_card)
        ], style={"marginTop": "30px"}
    )
], className="mt-12 container")

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
    elif pathname == '/analyze-file':
        return analyze_files.layout
    else:
        return app.layout
