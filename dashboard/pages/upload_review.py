""" Page layout for the explore data page. """
import dash_bootstrap_templates as dbt
from dash import dash_table, State
from dash import callback, Output, Input

from dashboard.functions import storage
from dashboard.functions.elements import *
from dashboard.functions.storage import get_categories, get_datastore_entities

dbt.load_figure_template(["bootstrap"])

# Overview
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Add a product review", className="display-3"),
            html.P(
                "Write a product review and send it to us! "
                "We will analyze it and give you a feedback.",
                className="lead",
            ),
            html.Hr(className="my-2"),
        ], fluid=True, className="py-3",
    ), className="p-3 bg-light rounded-3",
)

# Create a form to upload a review example
category_selector = dbc.Row(
    [
        dbc.Label("Select a category", html_for="category-selector", style={"font-size": "1.5em"}),
        dcc.Dropdown(
            id="category-selector",
            options=[{"label": category, "value": category} for category in get_categories()],
            value="",
            clearable=False,
            className="mb-3",
        ),
    ], className="mb-3",
)

title_input = dbc.Row(
    [
        dbc.Label("Title", html_for="title", style={"font-size": "1.5em"}),
        dbc.Input(id="title", type="text", placeholder="Enter a title"),
        dbc.FormText("Enter a title for the review example.", color="muted"),
        dbc.FormFeedback("This title seems a little bit odd.", type="invalid"),
        dbc.FormFeedback("This looks like a good title.", type="valid"),
    ], className="mb-3", style={"marginTop": "10px"}
)

product_id_input = dbc.Row(
    [
        dbc.Label("Product ID", html_for="product_id", style={"font-size": "1.5em"}),
        dbc.Input(id="product_id", type="text", placeholder="Enter a product ID"),
        dbc.FormText("Enter a product ID for the review example.", color="muted"),
        dbc.FormFeedback("Product ID is required.", type="invalid"),
    ], className="form-group", style={"marginTop": "10px"}
)

product_review_input = dbc.Row(
    [
        dbc.Label("Product review", html_for="product_review", style={"font-size": "1.5em"}),
        dbc.Textarea(id="product_review", placeholder="Enter a product review"),
        dbc.FormText("Enter a product review for the review example.", color="muted"),
        dbc.FormFeedback("Product review is required.", type="invalid"),
    ], className="form-group", style={"marginTop": "10px"}
)

product_rating_input = dbc.Row(
    [
        dbc.Label("Product rating", html_for="product_rating", style={"font-size": "1.5em"}),
        dcc.Slider(id="product_rating", min=1, max=5, step=1, value=3),
        dbc.FormText("Enter a product rating for the review example.", color="muted"),
        dbc.FormFeedback("Product rating is required.", type="invalid"),
    ], className="form-group", style={"marginTop": "10px"}
)

# Header
header = html.Div([
    dbc.Row(jumbotron, justify='center', style={"marginTop": "6px"}),
    dbc.Row(id='output-area', justify='center', style={"marginTop": "6px"}),
], className="mt-12 container")

# Main page layout
body = dbc.Card([
    dbc.CardBody(dbc.Form([category_selector, title_input, product_id_input,
                           product_review_input, product_rating_input])),
    dbc.CardFooter(dbc.Row([
        dbc.Col(dbc.Button("Submit", color="primary", className="mr-1", id="submit-button")),
        dbc.Col(dbc.Button("Reset", color="secondary", className="mr-1", id="reset-button")),
    ])),
], className="mt-12 container", style={"marginTop": "30px"})

layout = html.Div([navbar, header, body])


@callback(
    [Output("submit-button", "disabled"), Output("submit-button", "className")],
    [Input("category-selector", "value"), Input("title", "value"),
     Input("product_id", "value"), Input("product_review", "value")],
    prevent_initial_call=True,
)
def disable_submit_button(category, title, product_id, product_review):
    if category == "" or category is None or title == "" or title is None or product_id == "" or product_id is None:
        return True, "btn btn-primary disabled"
    else:
        return False, "btn btn-primary"


@callback(
    Output("reset-button", "disabled"),
    [Input("category-selector", "value"), Input("title", "value"),
     Input("product_id", "value"), Input("product_review", "value")],
    prevent_initial_call=True,
)
def disable_reset_button(category, title, product_id, product_review):
    if category == "" or title == "" or product_id == "" or product_review == "":
        return True
    else:
        return False


@callback(
    Output('title', 'valid'), Output('title', 'invalid'),
    [Input('title', 'value')],
    prevent_initial_call=True,
)
def validate_title(title):
    min_length = 3
    if check_for_string_length(title, min_length):
        return True, ''
    else:
        return False, 'Title is required111.'


def check_for_string_length(string, min_length):
    if len(string) < min_length:
        return False
    else:
        return True


@callback(
    [Output("category-selector", "value"), Output("title", "value"), Output("product_id", "value"),
     Output("product_title", "value"), Output("product_review", "value"), Output("product_rating", "value")],
    [Input("reset-button", "n_clicks")],
    prevent_initial_call=True,
)
def reset_form(n_clicks):
    if n_clicks > 0:
        return "", "", "", "", "", 3
