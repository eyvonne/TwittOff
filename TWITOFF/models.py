''' SQLAlchecmy models for twittoff'''

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    '''Twitter users that we pull and analyze'''
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)


class Tweet(DB.Model):
    '''tweets'''
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))


def addUser(name):
    DB.session.add(User(name=name))
    DB.session.commit()


def addTweet(text):
    DB.session.add(Tweet(text=text))
    DB.session.commit()
