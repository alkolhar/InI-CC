from dash import Dash
import dash_bootstrap_templates as dbt
import dash_bootstrap_components as dbc

# set default theme for plots
dbt.load_figure_template(["bootstrap"])
template_theme_light = "flatly"
url_theme_light = dbc.themes.FLATLY

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

app = Dash(__name__, external_stylesheets=[url_theme_light, dbc_css])

app.title = "Cloud computing: Review analysis"
