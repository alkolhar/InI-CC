""" Page layout for the explore data page. """
import dash_bootstrap_templates as dbt
from dash import dash_table
from dash import callback, Output, Input

from dashboard.functions import storage
from dashboard.functions.elements import *
from dashboard.functions.storage import get_categories, get_datastore_entities

dbt.load_figure_template(["bootstrap"])

# Overview
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Explore Categories", className="display-3"),
            html.P(
                "Choose a product category from the dropdown menu below "
                "and take a look at some review statistics.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            dbc.Row([
                dbc.Col(
                    dbc.Select(
                        id="select",
                        options=[
                            {'label': i, 'value': i} for i in get_categories()  # .unique()
                        ],
                        value='',
                    ), className="col-md-6"
                ),
                dbc.Col(
                    [
                        storage.download
                    ], className="d-grid gap-2 d-md-flex justify-content-md-end",
                )
            ], class_name="col-md-12"
            )
        ]
    )
)


@callback(
    Output('data_table', 'children'),
    [Input('select', 'value')],
)
def update_output(value):
    # Create a table for the data with the selected category
    df = get_datastore_entities(value)
    df = df[['date', 'rating', 'sentiment_score', 'review_text']]
    df = df.sort_values(by=['date'])
    df = df.reset_index(drop=True)
    df.dropna(subset=['rating'], inplace=True)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['rating'] = df['rating'].astype(str)
    df['sentiment_score'] = df['sentiment_score'].astype(str)
    df['review_text'] = df['review_text'].astype(str)
    table = dash_table.DataTable(
        df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
        id='tbl',
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        }
    ),
    return table


# Header
header = html.Div([
    dbc.Row(jumbotron, justify='center', style={"marginTop": "6px"}),
], className="mt-12 container")

# Main page layout
body = dcc.Loading(html.Div(id='data_table', className="mt-12 container"))

layout = html.Div([navbar, header, body])
