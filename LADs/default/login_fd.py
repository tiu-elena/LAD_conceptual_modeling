from dash import html, dcc
from dash.dependencies import Input, Output

from connection import app


layout = html.Div(children=[
    dcc.Location(id='url_login_df', refresh=True),
    html.Div(
        className="container",
        children=[
            html.Div(
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Br(),
                                html.Div('User non authenticated - Please login to view the success screen',
                                          style={'text-align': 'center', 'fontSize': 20}),
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            className="row",
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0,
                                            style={'text-align': 'center', 'fontSize': 20})
                            ],
                            style={'text-align': 'center', 'fontSize': 20}
                        )
                    ]
                )
            )
        ]
    )
])


@app.callback(Output('url_login_df', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
