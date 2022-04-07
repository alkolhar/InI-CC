from dashboard.index import app
import dash_bootstrap_components as dbc
from dash import html, dcc

import pandas as pd
import plotly.express as px

# Header
header = html.H4("Review Analysis", className="bg-primary text-white p-4 mb-2")

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
hist_review_count_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(id='hist_review_count', figure=hist_review_count)
            ]
        )
    ]
)

# create rating histogram
hist_ratings = px.histogram(df, x='rating', template="bootstrap", title='Review counts by rating')
hist_ratings.update_xaxes(categoryorder='total descending', title='Star rating').update_yaxes(title='Number of reviews')
hist_ratings_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(id='hist_ratings', figure=hist_ratings)
            ]
        )
    ]
)

# create time slide
fig = px.scatter(df, x='date', y='review_length', color="asin", hover_name="product_name", log_x=False)
scatter_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(id='scatter', figure=fig)
            ]
        )
    ]
)

# create boxplot rating by review length
box_rating = px.box(df, x="review_length", y="rating", color="rating", orientation='h')
box_rating_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(id='box_rating', figure=box_rating)
            ]
        )
    ]
)

app.layout = html.Div(
    [
        dbc.Row(header),
        dbc.Row(
            [
                dbc.Col(hist_review_count_card, width=5),
                dbc.Col(hist_ratings_card, width=5)
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
