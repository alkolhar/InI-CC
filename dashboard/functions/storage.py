import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Output, Input, State
from google.cloud import datastore

download = html.Div(
    [
        dbc.Button("Download .csv", id='btn_csv', outline=True, color="warning", className="me-md-2"),
        dcc.Download(id="download-dataframe-csv"),
        dbc.Button("Download .xslx", id='btn_xlsx', outline=True, color="success", className="me-md-2"),
        dcc.Download(id="download-dataframe-xlsx"),
    ]
)


@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State("select", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, category):
    if n_clicks is not None and category != '':
        df = get_datastore_entities(category)
        return dcc.send_data_frame(df.to_csv, "sentiment-analysis.csv")


@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    State("select", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, category):
    if n_clicks is not None and category != '':
        df = get_datastore_entities(category)
        # Remove timezone from columns
        df['date'] = df['date'].dt.tz_localize(None)
        return dcc.send_data_frame(df.to_excel, "sentiment-analysis.xlsx", sheet_name=category)


def get_categories():
    datastore_entities = datastore.Client().query(kind='category').fetch()
    return pd.DataFrame(datastore_entities)


def get_datastore_entities(category):
    datastore_entities = datastore.Client().query(kind=category).fetch()
    return pd.DataFrame(datastore_entities)

