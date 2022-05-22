from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from google.cloud import datastore
from dashboard.functions import settings


# This may help:
# https://stackoverflow.com/questions/36314797/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery
def demo_datastore():
    # Create, populate and persist an entity with keyID=1234
    client = datastore.Client()
    key = client.key('EntityKind', 1234)
    entity = datastore.Entity(key=key)
    entity.update({
        'foo': u'bar',
        'baz': 1337,
        'qux': False,
    })
    client.put(entity)
    # Then get by key for this entity
    result = client.get(key)
    print(result)


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
    prevent_initial_call=True,
)
def func(n_clicks):
    df = settings.df
    return dcc.send_data_frame(df.to_csv, "sentiment-analysis.csv")


@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    df = settings.df
    return dcc.send_data_frame(df.to_excel, "sentiment-analysis.xlsx", sheet_name="Sheet_name_1")
