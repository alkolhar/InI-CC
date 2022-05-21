import dash_bootstrap_templates as dbt

from dashboard.functions.elements import *

dbt.load_figure_template(["bootstrap"])

# Data preprocessing
# TODO: Pfad für GCP anpassen
df = pd.read_xml('E:/Repositories/InI-CC/data/kitchen_&_housewares/unlabeled.xml')
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
scatter_card = create_scatter_plot(df, 'date', 'review_length', 'asin', 'product_name')

# create boxplot rating by review length
box_rating_card = create_boxplot(df, 'review_length', 'rating', 'rating', 'h')

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
            html.P(
                dbc.Row(dbc.DropdownMenu(
                    label="Choose a category",
                    children=[
                        dbc.DropdownMenuItem("1"),
                        dbc.DropdownMenuItem("2"),
                        dbc.DropdownMenuItem("3")
                    ]),
                    class_name="col-md-6"),
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
        )
    ], className="mt-12 container"
)

layout = html.Div([navbar, body])
