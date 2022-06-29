import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, dcc, State

from dashboard.functions.analyze import upload_review_file
from dashboard.functions.elements import navbar

empty_string = "As soon as your file has reached our server, one of your uploaded reviews can be read here."
initial_return = ("--", "--", html.Div([empty_string]))

input_section = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Upload a file to analyse")
        ),
        dbc.CardBody(
            [
                html.Div(empty_string, id='example_review')
            ]
        ),
        dbc.CardFooter(
            [
                dcc.Upload(
                    id='upload-file',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    }
                )
            ]
        )
    ]
)


@callback(
    Output("example_review", "children"),
    Output("rev-count", "children"),
    Output("word-count", "children"),
    Input("upload-file", "contents"),
    State("upload-file", "filename"),
    State("upload-file", "last_modified")
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        return upload_review_file(list_of_contents, list_of_names, list_of_dates)
    else:
        raise dash.exceptions.PreventUpdate


output_section = dcc.Loading(
    dbc.Card(
        [
            dbc.CardHeader(
                html.H5("Uploaded files statistics")
            ),
            dbc.CardBody(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("No. of Reviews", className='text-center')
                                ),
                                dbc.CardBody(
                                    html.H2("--", id="rev-count", className='text-center')
                                )
                            ], color="primary", outline=True
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("Word count", className='text-center')
                                ),
                                dbc.CardBody(
                                    html.H2("--", id="word-count", className='text-center')
                                )
                            ], color="primary", outline=True
                        )
                    )
                ]
            )
        ]
    )
)

body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(input_section),
                dbc.Col(output_section, class_name="col-md-4")
            ], justify="center"
        ),
        dbc.Row(
            html.Div(id='out_analyse'), style={"marginTop": "30px"}, class_name="col-md-12"
        )
    ], className="mt-12 container", style={"marginTop": "30px"}
)

layout = html.Div([navbar, body])
