from dash import html
import dash_bootstrap_components as dbc

from dashboard.functions.elements import navbar

card = dbc.Card(
    [
        dbc.CardHeader(
            html.H5("Insert text to analyze")
        ),
        dbc.CardBody(
            dbc.Textarea(size="lg", placeholder="A large Textarea", rows=8, className="card-text")
        ),
        dbc.CardFooter(
            dbc.Button("Analyze", color="primary")
        )
    ]
)

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
                                    )
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
                                            html.H2("17", className='text-center')
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
                                            html.H2("69", className='text-center')
                                        )
                                    ]
                                ), style={"margin-top": "6px"}
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
    ], className="mt-12 container", style={"margin-top": "30px"}
)

layout = html.Div([navbar, body])
