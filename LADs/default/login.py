from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc, html

from flask_login import login_user

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json

import connection
from connection import app
from flask import session

import bcrypt

import datetime
import dash_daq as daq

import random


with open("../data/hashes.json", "r") as f:
    creds_data = json.load(f)


layout = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Br(),
                html.Img(id='image-logo', src = '/assets/logo.png',
                                                    style={'width': '180px', 'height': '180px',
                                                           'display': 'block','margin-left': 'auto','margin-right': 'auto','textAlign':'center'}, 
                                                    ),
                html.Br(),                                    
                html.Div('''Please log in to continue:''', id='h1',  style={'text-align': 'center', 'fontSize': 20}),
                html.Div(
                    children=[
                        html.Br(),
                        dcc.Input(
                            placeholder='Enter your username',
                            n_submit=0,
                            type='text',
                            id='uname-box'
                        ),
                        html.Br(),
                        dcc.Input(
                            placeholder='Enter your password',
                            n_submit=0,
                            type='password',
                            id='pwd-box'
                        ),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button',
                            style={'text-align': 'center', 'fontSize': 16}
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div(children='', id='output-state', style={'color':'red'})
                    ],
                     style={'textAlign': 'center'}
                ),
            ]
        )
    ]
)


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def find_next_empty_row(worksheet, start_row=1, column=1):
    """Find the index of the next empty row in a specific column."""
    for row in range(start_row, worksheet.max_row + 1):
        if worksheet.cell(row, column).value is None:
            return row
    return worksheet.max_row + 1


@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')
               ],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')]
               )
def success(n_clicks, login, password):
    if n_clicks > 0 and (login is not None) and (password is not None):
        psw_hash = creds_data[login]
        if psw_hash:
            if verify_password(password, psw_hash):

                user = connection.User(id = login)
                login_user(user)
                print(f'Current user is {user.id}')

                session_id = ''.join(random.choices('0123456789', k=6))
                session['id'] = session_id
                session['type'] = 'master-only'
                return '/success'

            else:
                pass
        else:
            pass
    else:
        pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks'),
               Input('uname-box', 'value'),
               Input('pwd-box', 'value')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    if n_clicks > 0 and (n_submit_uname and n_submit_pwd):
        psw_hash = creds_data[input1]
        if psw_hash:
            if verify_password(input2, psw_hash):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        n_clicks = 0
        return ''