from dash import Dash
import os
from flask_login import LoginManager, UserMixin
import flask
from datetime import timedelta
import dash_bootstrap_components as dbc

server = flask.Flask(__name__)
app = Dash(__name__, 
           meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.8, maximum-scale=1.2, minimum-scale=0.5,'}],
                            server=server,     
                            external_stylesheets=[dbc.themes.BOOTSTRAP]    
        )

app.title = "AMMIS dashboard"

server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server.config.update(
    SECRET_KEY=os.urandom(12),
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
)


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin):
    def __init__(self, id, active=True):
        self.id = id
        self.active = active

    def is_active(self):

        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    
@login_manager.user_loader
def load_user(user_id):
    return User(id =user_id)