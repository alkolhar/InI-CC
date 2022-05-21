from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from dashboard.functions.analyze import analyze_string_dummy
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
    ]
)


@callback(
    Output("mag", "children"),
    Output("score", "children"),
    Input("btn-analyze", "n_clicks"),
    Input("txt_area", "value")
)
def btn_click(n, value):
    if n is None:
        return "--", "--"
    else:
        analyze_string_dummy(value)
        return "Mag", "Score"  # TODO: return magnitude and score


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
                                    ]
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
                                    ]
                                ), style={"marginTop": "6px"}
                            )
                        ]
                    )
                ]
            )
        )
    ]
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
