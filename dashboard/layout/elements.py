import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import plotly.express as px

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analyse Text", href="/page2")),
        dbc.NavItem(dbc.NavLink("Explore", href="/page1"))
    ],
    brand="Review Sentiment Analysis",
    brand_href="/",
    color="primary",
    dark=True,
)


def create_hist_plot(df: pd.DataFrame, x_value: str, plot_title: str, x_title: str = '', y_title: str = '',
                     order: str = 'total descending') -> (dbc.Card, id):
    hist = px.histogram(df, x=x_value, template="bootstrap", title=plot_title)
    hist.update_xaxes(categoryorder=order, title=x_title).update_yaxes(title=y_title)
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='hist', figure=hist)
                ]
            )
        ]
    )


def create_scatter_plot(df: pd.DataFrame, x_value: str, y_value: str, color: str, hover_name: str, log_x: bool = False):
    fig = px.scatter(df, x=x_value, y=y_value, color=color, hover_name=hover_name, log_x=log_x)
    return dbc.Card(
        [
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
            dbc.CardBody(
                [
                    dcc.Graph(id='box_rating', figure=box_rating)
                ]
            )
        ]
    )
