import dash_bootstrap_templates as dbt

from dashboard.functions import storage
from dashboard.functions.elements import *

dbt.load_figure_template(["bootstrap"])

# create count on number of reviews per product
hist_review_count = create_hist_plot('asin', 'Review counts by product', 'Product Number',
                                     'Number of reviews', 'total descending')

# create rating histogram
hist_ratings = create_hist_plot('rating', 'Review counts by rating', 'Star rating',
                                'Number of reviews', 'total descending')

# create scatter over time
scatter_card = create_scatter_plot('date', 'review_length', 'asin', 'product_name')

# create boxplot rating by review length
box_rating_card = create_boxplot('review_length', 'rating', 'rating', 'h')

# create word cloud
word_cloud_card = create_wordcloud()

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
                                {'label': i, 'value': i} for i in settings.opt['options'].unique()
                            ],
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

# Main page layout
body = html.Div(
    [
        dbc.Row(jumbotron, style={"marginTop": "6px"}),
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
    ], className="mt-12 container"
)

layout = html.Div([navbar, body])
