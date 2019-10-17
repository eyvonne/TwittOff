'''Main application for twittoff'''

# imports
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user


def create_app():
    '''creates and configures an instance of a flask app'''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # app.config['ENV'] = config('ENV')  # should change this later to production
    app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
            # tweets = []
        except Exception as e:
            message = 'error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themself'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

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
