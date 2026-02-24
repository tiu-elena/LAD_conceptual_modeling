from dash.dependencies import Input, Output
from dash import html, dcc

from flask_login import logout_user, current_user

import login, login_fd, logout
# from login import logs_data

from connection import app, server
import success_master
from flask import session


header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)

app.layout = html.Div(
    [
        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return success_master.layout

        else:
            return login.layout
    elif pathname == '/login':
        if current_user.is_authenticated:
            return success_master.layout

        else:
            return login.layout

    elif pathname == '/success': 
        if current_user.is_authenticated:

            return success_master.layout

        else:
            return login_fd.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            logout_user()
            return logout.layout
    else:
        if current_user.is_authenticated:

            return success_master.layout

        else:
            return '404'


if __name__ == '__main__':
    app.run(debug=True)