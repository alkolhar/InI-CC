import dash_bootstrap_templates as dbt
import pandas as pd
from dash import callback, Output, Input

from dashboard.functions import storage
from dashboard.functions.elements import *
from dashboard.functions.storage import get_categories, get_datastore_entities

dbt.load_figure_template(["bootstrap"])


# Overview
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Explore Datasets", className="display-3"),
            html.P(
                "Choose a product category from the dropdown menu below "
                "and take a look at some review statistics.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            # TODO: reload settings.opt dataframe
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Select(
                            id="select",
                            options=[
                                {'label': i, 'value': i} for i in get_categories()  # .unique()
                            ],
                            value='book',
                        ), className="col-md-6"
                    ),
                    dbc.Col(
                        [
                            storage.download
                        ], className="d-grid gap-2 d-md-flex justify-content-md-end",
                    )
                ], class_name="col-md-12"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)


# Update site layout depending on the selected product category
@callback(
    Output('explore_df', 'children'),
    [Input('select', 'value')]
)
def update_output(value):
    df = get_datastore_entities(value)

    # create count on number of reviews per product
    hist_review_count = create_hist_plot(df, 'asin', 'Review counts by product', 'Product Number',
                                         'Number of reviews', 'total descending')
    # create rating histogram
    hist_ratings = create_hist_plot(df, 'rating', 'Review counts by rating', 'Star rating',
                                    'Number of reviews', 'total descending')
    # create scatter over time
    scatter_card = create_scatter_plot(df, 'date', 'review_length', 'asin', 'product_name')
    # create boxplot rating by review length
    box_rating_card = create_boxplot(df, 'review_length', 'rating', 'rating', 'h')
    # create word cloud
    word_cloud_card = create_wordcloud(df)

    return [
        dbc.Row(
            [
                dbc.Col(hist_review_count, width=6),
                dbc.Col(hist_ratings, width=6)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(scatter_card, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(box_rating_card, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(word_cloud_card, width=12)
            ], justify='center', style={"marginTop": "30px", "maxHeight": "300px"}
        )
    ]


# Header
header = html.Div([
    dbc.Row(jumbotron, style={"marginTop": "6px"})
], className="mt-12 container")

# Main page layout
body = html.Div(id='explore_df', className="mt-12 container")

layout = html.Div([navbar, header, body])
