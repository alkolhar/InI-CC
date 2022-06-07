import dash_bootstrap_templates as dbt
from dash import callback, Output, Input

from dashboard.functions import storage
from dashboard.functions.elements import *

dbt.load_figure_template(["bootstrap"])

# Overview
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Explore Products", className="display-3"),
            html.P(
                "Choose a product from the dropdown menu below "
                "and take a look at some sentiment statistics.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            # TODO: reload settings.opt dataframe
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Select(
                            id="select-category",
                            options=[
                                {'label': i, 'value': i} for i in settings.opt['options'].unique()
                            ],
                            value='book',
                        ), className="col-md-4"
                    ),
                    dbc.Col(
                        dbc.Select(
                            id="select-product",
                            options=[
                                {'label': i, 'value': i} for i in settings.opt['options'].unique()
                            ],
                            value='',
                        ), className="col-md-4"
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
    Output('explore_product', 'children'),
    [Input('select-product', 'value')]
)
def update_output(value):
    print(value)


@callback(
    Output("select-product", "options"),
    [Input("select-product", "search_value"), Input("select-category", "value")],
)
def set_dropdown_content(search_value, cat_dd):
    if cat_dd is not None:
        settings.df = settings.reload_df(cat_dd)
        return [{"label": i, "value": i} for i in settings.df['asin'].unique()]


# Header
header = html.Div([
    dbc.Row(jumbotron, style={"marginTop": "6px"})
], className="mt-12 container")

# Main page layout
body = html.Div(id='explore_product', className="mt-12 container")

layout = html.Div([navbar, header, body])
