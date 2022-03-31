from aio import ThemeSwitchAIO
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt
import plotly.express as px
import plotly.io as pio
import pandas as pd

# set default theme for plots
dbt.load_figure_template(["bootstrap"])
template_theme_light = "flatly"
template_theme_dark = "darkly"
url_theme_light = dbc.themes.FLATLY
url_theme_dark = dbc.themes.DARKLY
dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

# Header
header = html.H4("REview Analysis", className="bg-primary text-white p-4 mb-2")

# Data preprocessing
df = pd.read_xml('./data/kitchen_&_housewares/unlabeled.xml')
# make dates great again
df['date'] = pd.to_datetime(df['date'])
# calculate review character length
df['review_length'] = df['review_text'].str.len()

# create count on number of reviews per product
hist_review_count = px.histogram(df, x='asin', template="bootstrap", title='Review counts by product')
hist_review_count.update_xaxes(categoryorder='total descending', title='Product Number').update_yaxes(
    title='Number of reviews')

# create rating histogram
hist_ratings = px.histogram(df, x='rating', template="bootstrap", title='Review counts by rating')
hist_ratings.update_xaxes(categoryorder='total descending', title='Star rating').update_yaxes(title='Number of reviews')

# create time slide
fig = px.scatter(df, x='date', y='rating', size="review_length", color="asin", hover_name="product_name", log_x=False,
                 size_max=60)


def generate_table(dataframe, max_rows=10):
    return html.Table([html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])), html.Tbody(
        [html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in
         range(min(len(dataframe), max_rows))])])


app = Dash(__name__, external_stylesheets=[url_theme_light, dbc_css])

app.layout = html.Div([
        dbc.Row(header),
        dbc.Row(ThemeSwitchAIO(aio_id="theme", themes=[url_theme_light, url_theme_dark])),
        dbc.Row(dbc.Col(generate_table(df), width={'size': 10, 'offset': 1})),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hist_review_count', figure=hist_review_count),
                    width=8, lg={'size': 6, 'offset': 0, 'order': 'first'}),
            dbc.Col(dcc.Graph(id='hist_ratings', figure=hist_ratings),
                    width=8, lg={'size': 6, 'offset': 0, 'order': 'first'})
        ]),
        dbc.Row(dcc.Graph(id='fig', figure=fig))
    ])


@app.callback(
    Output("fig", "figure"), Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_graph_theme(toggle):
    template = template_theme_light if toggle else template_theme_dark
    return px.scatter(df, x='date', y='rating', size="review_length", template=template, hover_name="product_name",
                      log_x=False, size_max=60)


if __name__ == "__main__":
    app.run_server(debug=True)
