import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import plotly.express as px

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analyze Strings", href="/analyze-str"), style={"margin-left": "5px"}),
        dbc.NavItem(dbc.NavLink("Explore Dataset", href="/explore"), style={"margin-left": "5px"})
    ],
    brand="Review Sentiment Analysis",
    brand_href="/",
    color="primary",
    dark=True,
)


def create_hist_plot(df: pd.DataFrame, x_value: str, plot_title: str, x_title: str = '', y_title: str = '',
                     order: str = 'total descending') -> dbc.Card:
    hist = px.histogram(df, x=x_value, template="bootstrap")
    hist.update_xaxes(categoryorder=order, title=x_title).update_yaxes(title=y_title)
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5(plot_title)
            ),
            dbc.CardBody(
                [
                    dbc.Row(dbc.DropdownMenu(
                        label="Choose a category",
                        children=[
                            dbc.DropdownMenuItem("1")
                        ]),
                        class_name="col-md-6"),
                    dcc.Graph(id='hist', figure=hist)
                ]
            )
        ]
    )


def create_scatter_plot(df: pd.DataFrame, x_value: str, y_value: str, color: str, hover_name: str, log_x: bool = False):
    fig = px.scatter(df, x=x_value, y=y_value, color=color, hover_name=hover_name, log_x=log_x)
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5("Review lengths over time")
            ),
            dbc.CardBody(
                [
                    dcc.Graph(id='scatter', figure=fig)
                ]
            )
        ]
    )


def create_boxplot(df: pd.DataFrame, x_value: str, y_value: str, color: str, orientation: str):
    box_rating = px.box(df, x=x_value, y=y_value, color=color, orientation=orientation)
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5("Boxplot of ratings")
            ),
            dbc.CardBody(
                [
                    dcc.Graph(id='box_rating', figure=box_rating)
                ]
            )
        ]
    )
