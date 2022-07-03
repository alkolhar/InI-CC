import logging

import dash_bootstrap_templates as dbt
import pandas as pd
from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate

from dashboard.functions.elements import *
from dashboard.functions.storage import get_categories, get_datastore_entities

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
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Select(
                            id="select-category",
                            options=[
                                {'label': i, 'value': i} for i in get_categories()
                            ],
                            value='',
                            placeholder="Select a category",
                        ), className="col-md-4"
                    ),
                    dbc.Col(
                        dbc.Select(
                            id="select-product",
                            options=[],
                            value='',
                        ), className="col-md-4"
                    ),
                ], class_name="col-md-12"
            ),
            dcc.Store(id="intermediate-value")
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)


# Update dropdown values depending on the selected product category
@callback(
    Output("select-product", "options"),
    [Input("select-category", "value")],
)
def set_dropdown_content(cat_dd):
    if cat_dd is not None:
        dff = get_datastore_entities(cat_dd)
        return [{"label": i, "value": i} for i in dff['product_id'].unique()]


@callback(
    Output("select-category", "options"),
    Input("select-category", "search_value"),
    State("select-category", "options"),
)
def update_options(search_value, options):
    if not search_value:
        raise PreventUpdate
    return [o for o in options if search_value in o['label']]


# Update site layout depending on the selected product
@callback(
    Output('intermediate-value', 'data'),
    Input('select-product', 'value'),
    State('select-category', 'value'),
    prevent_initial_call=True
)
def update_output(prod_id, cat_dd):
    dff = get_datastore_entities(cat_dd)

    if isinstance(prod_id, str) and prod_id != '':
        dff = dff[dff.product_id == prod_id]
        return dff.to_json()


@callback(
    Output('prod_title', 'children'), Output('prod_id', 'children'), Output('prod_summary', 'children'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_text(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # return product id and count of all reviews for this product
        prd_name = str(dff.iloc[0]['product_name'])
        prd_id = 'Product: ' + str(dff.iloc[0]['product_id'])
        prd_sum = 'We currently have '
        sums = len(dff)
        if sums == 1:
            prd_sum = prd_sum + '1 review for this product.'
        else:
            prd_sum = prd_sum + str(sums) + ' reviews for this product.'

        return prd_name, prd_id, prd_sum
    else:
        logging.info('no data')


@callback(
    Output('hist1_l', 'figure'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_hist1_l(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # update graphs in body with new data
        fig = px.histogram(dff, x='rating', template=def_template, color='rating', nbins=10)
        return fig
    else:
        logging.info('no data')


@callback(
    Output('hist1_r', 'figure'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_hist1_r(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # update graphs in body with new data
        fig = px.histogram(dff, x='sentiment_score', template=def_template, color='rating', nbins=4)
        return fig
    else:
        logging.info('no data')


@callback(
    Output('prod_scatter', 'figure'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_prod_scatter(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # update graphs in body with new data
        fig = px.scatter(dff, x='date', y='review_length', color='sentiment_score',
                         hover_name='product_name', template=def_template)
        return fig
    else:
        logging.info('no data')


@callback(
    Output('prod_box', 'figure'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_prod_box(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # update graphs in body with new data
        fig = px.box(dff, x='review_length', y='rating', color='rating', orientation='h', template=def_template)
        return fig
    else:
        logging.info('no data')


@callback(
    Output('wc_img', 'children'),
    Input('intermediate-value', 'data'),
    prevent_initial_call=True)
def update_prod_box(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data)
        # update wordcloud in body with new data
        return create_wordcloud(dff)
    else:
        logging.info('no data')


header = html.Div([
    dbc.Row(jumbotron, style={"marginTop": "6px"})
], className="mt-12 container")

# Main page layout
body = html.Div([
    dcc.Loading([
        dbc.Row([
            html.H3(id='prod_title'),
            html.Small(id='prod_id'),
        ]),
        dbc.Row([
            html.H5(id='prod_summary'),
        ])
    ], type="circle", color="primary"),
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5('Histogram of ratings'),
                    ),
                    dbc.CardBody(
                        [dbc.Spinner(dcc.Graph(id='hist1_l'))]
                    )
                ], color="primary", outline=True
            ), width=6),
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5('Histogram of sentiment scores'),
                    ),
                    dbc.CardBody(
                        [dbc.Spinner(dcc.Graph(id='hist1_r'))]
                    )
                ], color="primary", outline=True
            ), width=6)
        ], justify="center", style={"marginTop": "30px"}
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Review lengths over time")
                    ),
                    dbc.CardBody(
                        [dbc.Spinner(dcc.Graph(id='prod_scatter'))]
                    )
                ], color="primary", outline=True
            ), width=12)
        ], justify="center", style={"marginTop": "30px"}
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Ratings distribution")
                    ),
                    dbc.CardBody(
                        [dbc.Spinner(dcc.Graph(id='prod_box'))]
                    )
                ], color="primary", outline=True
            ), width=12)
        ], justify="center", style={"marginTop": "30px"}
    ),
    dbc.Row(
        [dbc.Spinner(dbc.Col(id='wc_img', width=12))],
        justify='center', style={"marginTop": "30px", "maxHeight": "300px"}
    )
], id='explore_prod', className="mt-12 container")

layout = html.Div([navbar, header, body])
