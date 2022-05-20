import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt

from dashboard.layout.elements import *

dbt.load_figure_template(["bootstrap"])

# Data preprocessing
# TODO: Pfad für GCP anpassen
df = pd.read_xml('C:/Repositories/InI-CC/data/kitchen_&_housewares/unlabeled.xml')
# make dates great again
df['date'] = pd.to_datetime(df['date'])
# calculate review character length
df['review_length'] = df['review_text'].str.len()

# create count on number of reviews per product
hist_review_count = create_hist_plot(df, 'asin', 'Review counts by product', 'Product Number',
                                     'Number of reviews', 'total descending')

# create rating histogram
hist_ratings = create_hist_plot(df, 'rating', 'Review counts by rating', 'Star rating',
                                'Number of reviews', 'total descending')

# create scatter over time
scatter_card = create_scatter_plot(df, 'date', 'review_length', 'asin', 'product')

# create boxplot rating by review length
box_rating_card = create_boxplot(df, 'review_length', 'rating', 'rating', 'h')


# Main page layout
body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(hist_review_count, width=5),
                dbc.Col(hist_ratings, width=5)
            ], justify="center"
        ),
        dbc.Row(
            [
                dbc.Col(scatter_card, width=10)
            ], justify="center"
        ),
        dbc.Row(
            [
                dbc.Col(box_rating_card, width=10)
            ], justify="center"
        )
    ]
)

layout = html.Div([navbar, body])
