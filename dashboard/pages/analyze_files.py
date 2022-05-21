import dash
from dash import html, callback, Output, Input, dcc, State
import dash_bootstrap_components as dbc

from dashboard.functions.analyze import analyze_string_dummy, analyze_file_dummy, analyze_file
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
                ),
                html.Div(
                    [
                        dbc.Button("Analyse", id="btn-analyse", color="primary", className="me-1")
                    ]
                )
            ]
        )
    ]
)


@callback(
    Output("example_review", "children"),
    Output("rev-count", "children"),
    Output("word-count", "children"),
    Output("rev-cat", "children"),
    Input("upload-file", "contents"),
    State("upload-file", "filename"),
    State("upload-file", "last_modified")
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        return analyze_file_dummy(list_of_contents, list_of_names, list_of_dates)  # TODO: return magnitude and score
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output("out_analyse", "children"),
    Input("btn-analyse", "n_clicks")
)
def list_analysis(n):
    print(n)
    if n is None:
        return "No Analysis done yet!"
    else:
        return analyze_file()


output_section = dbc.Card(
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
                                html.H4("No. of Products", className='text-center')
                            ),
                            dbc.CardBody(
                                html.H2("--", id="rev-cat", className='text-center')
                            )
                        ]
                    ), style={"marginTop": "6px"}
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("No. of Reviews", className='text-center')
                            ),
                            dbc.CardBody(
                                html.H2("--", id="rev-count", className='text-center')
                            )
                        ]
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
                        ]
                    )
                )
            ]
        )
    ]
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
            html.P(id='out_analyse'), style={"marginTop": "30px"}, class_name="col-md-12"
        )
    ], className="mt-12 container", style={"marginTop": "30px"}
)

layout = html.Div([navbar, body])