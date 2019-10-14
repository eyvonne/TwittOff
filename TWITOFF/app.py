'''Main application for twittoff'''

# imports
from flask import Flask
from .models import DB


def create_app():
    '''creates and configures an instance of a flask app'''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'welcome to the app'
    return app
