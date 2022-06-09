from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

from dashboard.functions.analyze import analyze_string
from dashboard.functions.elements import navbar

card = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Insert text to analyze")
        ),
        dbc.CardBody(
            dbc.Textarea(id="txt_area", size="lg", placeholder="A large Textarea", rows=8, className="card-text")
        ),
        dbc.CardFooter(
            dbc.Button("Analyze", id="btn-analyze", color="primary")
        )
    ], color="primary", outline=True
)


@callback(
    Output("mag", "children"),
    Output("score", "children"),
    Input("btn-analyze", "n_clicks"),
    State("txt_area", "value")
)
def btn_click(n, value):
    if n is None:
        return "--", "--"
    else:
        score, mag = analyze_string(value)
        return "{:.2f}".format(mag), "{:.2f}".format(score)


output = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Results")
        ),
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(src="/static/images/portrait-placeholder.png",
                                    className="img-fluid rounded-start",
                                    )  # TODO: change image
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H3("Magnitude", className='text-center')
                                        ),
                                        dbc.CardBody(
                                            html.H2("17", id="mag", className='text-center')
                                        )
                                    ], color="primary", outline=True
                                )
                            ),
                            dbc.Row(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H3("Score", className='text-center')
                                        ),
                                        dbc.CardBody(
                                            html.H2("69", id="score", className='text-center')
                                        )
                                    ], color="primary", outline=True
                                ), style={"marginTop": "6px"}
                            )
                        ]
                    )
                ]
            )
        )
    ], color="primary", outline=True
)

body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card),
                dbc.Col(output, class_name="col-md-4")
            ], justify="center"
        )
    ], className="mt-12 container", style={"marginTop": "30px"}
)

layout = html.Div([navbar, body])
