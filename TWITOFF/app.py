'''Main application for twittoff'''

# imports
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User


def create_app():
    '''creates and configures an instance of a flask app'''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')  # should change this later to production
    app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', users=[])
#    @app.route('/factor/<int:number>')
#    def factor(number):
#        try:
#            num = int(number
#            factors=[]
#            for i in range(num):
#                if num % i == 0:
#                    factors.append(i)
#            return factors
#        except:
#            return 'not a number'
#        return number
    return app
