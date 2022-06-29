import datetime

import dash_bootstrap_templates as dbt
from dash import callback, Output, Input, State, dash_table

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
            ),
            html.Hr(className="my-2"),
            dbc.Row([
                dbc.Button("Show Filters", id="filter_button", color="primary"),
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Filter by rating:", className="text-center"),
                            dcc.RangeSlider(1, 5, 1, value=[1, 5], id='rating_slider')
                        ], width=6),
                        dbc.Col([
                            html.H5("Filter by sentiment:", className="text-center"),
                            dcc.RangeSlider(-1, 1, 0.1, value=[-1, 1], id='sentiment_slider'),
                        ], width=6),
                    ]),
                    dbc.Row([
                        html.H5("Filter by date:", className="text-center"),
                        dcc.DatePickerRange(id='date_picker', clearable=True,
                                            min_date_allowed=datetime.datetime(2000, 1, 1),
                                            max_date_allowed=datetime.datetime(2008, 1, 1),
                                            initial_visible_month=datetime.datetime(2000, 1, 1),
                                            start_date=datetime.datetime(2000, 1, 1),
                                            end_date=datetime.datetime(2008, 1, 1)),
                    ], justify="center", className="col-md-6"),
                ], id='filter_collapse', is_open=False, className="mt-3"),
            ], className="d-grid gap-2 d-md-flex justify-content-md-end")
        ], fluid=True, className="py-3",
    ), className="p-3 bg-light rounded-3",
)


# Update site layout depending on the selected product category
@callback(
    [Output('explore_df', 'children'),
     Output('table', 'columns'), Output('table', 'data'), Output('table', 'tooltip_data')],
    [Input('select', 'value'),
     Input('date_picker', 'start_date'), Input('date_picker', 'end_date'),
     Input('rating_slider', 'value'), Input('sentiment_slider', 'value')],
)
def update_output(value, start_date, end_date, rating_slider, sentiment_slider):
    if value == '':
        child = html.Div('Please select a category first.', className="text-center", style={"marginTop": "30px"})
        return child, [], [], []
    df = get_datastore_entities(value)
    df['rating'] = df['rating'].astype(float)
    if start_date is not None and end_date is not None:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    if rating_slider is not None:
        df = df[(df['rating'] >= rating_slider[0]) & (df['rating'] <= rating_slider[1])]
    if sentiment_slider is not None:
        df = df[(df['sentiment_score'] >= sentiment_slider[0]) & (df['sentiment_score'] <= sentiment_slider[1])]

    dff = prepare_data_for_table(df)
    # Update values in dash data table
    new_table = [{"name": i, "id": i} for i in dff.columns]
    new_data = dff.to_dict('records')
    new_tooltip_data = [{
        'sentiment_score': {'value': row['review_text'], 'type': 'markdown'}
    } for row in df.to_dict('records')]

    # create count on number of reviews per product
    hist_review_count = create_hist_plot(df, 'product_id', 'Review counts by product', 'Product Number',
                                         'Number of reviews', 'total descending')
    # create rating histogram
    hist_ratings = create_hist_plot(df, 'rating', 'Review counts by rating', 'Star rating',
                                    'Number of reviews', 'total descending')
    # create scatter over time
    scatter_card = create_scatter_plot(df, 'date', 'review_length', 'product_id', 'product_name',
                                       'Review lengths over time')
    # create sentiment histogram
    hist_sentiment = create_hist_plot(df, 'sentiment_score', 'Review counts by sentiment', 'Sentiment score',
                                      'Number of reviews', 'total descending')
    # create sentiment scatter
    scatter_sentiment = create_scatter_plot(df, 'date', 'sentiment_score', 'product_id', 'product_name',
                                            'Sentiment over time')
    # create boxplot rating by review length
    box_rating_card = create_boxplot(df, 'review_length', 'rating', 'rating', 'h', "Boxplot of ratings")
    # create boxplot sentiment by review length
    box_sentiment_card = create_boxplot(df, 'sentiment_score', 'rating', 'rating', 'h',
                                        "Sentiment score")
    # create word cloud
    word_cloud_card = create_wordcloud(df)

    # metrics
    ssc = df['sentiment_score'].mean()
    ssc_text = 'Neutral'
    rsc = df['rating'].mean()
    rsc_text = 'Neutral'
    if ssc > 0:
        ssc_text = 'Positive'
        if ssc > 0.5:
            ssc_text = 'Very positive'
    elif ssc < 0:
        ssc_text = 'Negative'
        if ssc < -0.5:
            ssc_text = 'Very negative'

    if rsc > 3:
        rsc_text = 'Seems to be a good category'
    elif rsc < 3:
        rsc_text = 'Seems to be a bad category'

    child = [
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Number of reviews", className="text-center")),
                dbc.CardBody(html.H3(str(len(df))), className="text-center"),
                dbc.CardFooter(html.Small(str(df['product_id'].nunique()) + ' different products'),
                               className="text-center")
            ])),
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Average Rating", className="text-center")),
                dbc.CardBody(html.H3('{0:.3g}'.format(rsc)), className="text-center"),
                dbc.CardFooter(html.Small(rsc_text), className="text-center")
            ])),
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Average Sentiment", className="text-center")),
                dbc.CardBody(html.H3('{0:.3g}'.format(ssc), className="text-center")),
                dbc.CardFooter(html.Small(ssc_text), className="text-center")
            ]))
        ]),
        dbc.Row(
            [
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H5("Dataset")),
                    dbc.CardBody(table)
                ], color="primary", outline=True
                ))
            ], justify="center", style={"marginTop": "30px"}),
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
                dbc.Col(hist_sentiment, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(scatter_sentiment, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(box_rating_card, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(box_sentiment_card, width=12)
            ], justify="center", style={"marginTop": "30px"}
        ),
        dbc.Row(
            [
                dbc.Col(word_cloud_card, width=12)
            ], justify='center', style={"marginTop": "30px", "maxHeight": "300px"}
        )
    ]
    return child, new_table, new_data, new_tooltip_data


@callback(
    Output("filter_collapse", "is_open"),
    [Input("filter_button", "n_clicks")],
    [State("filter_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# create empty dash data table
table = dash_table.DataTable(
    id='table',
    columns=[],
    editable=False,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=10,
    tooltip_duration=None,
    style_cell={
        'textOverflow': 'ellipsis',
        'overflow': 'hidden',
        'maxWidth': 0,
        'textAlign': 'left',
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'},
    style_cell_conditional=[
        {'if': {'column_id': 'date'}, 'width': '12%'},
        {'if': {'column_id': 'product_id'}, 'width': '12%'},
        {'if': {'column_id': 'reviewer'}, 'width': '20%'},
        {'if': {'column_id': 'rating'}, 'width': '7%', 'textAlign': 'right'},
        {'if': {'column_id': 'sentiment_score'}, 'width': '12%', 'textAlign': 'right'},
    ],
    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'color': 'white'},
)

# Header
header = html.Div([
    dbc.Row(jumbotron, justify='center', style={"marginTop": "6px"}),
], className="mt-12 container")

# Main page layout
body = dcc.Loading([
    html.Div(table, id='table', className="mt-12 container"),
    html.Div(id='tbl_out', className="mt-12 container"),
    html.Div(id='explore_df', className="mt-12 container"),
])

layout = html.Div([navbar, header, body])
