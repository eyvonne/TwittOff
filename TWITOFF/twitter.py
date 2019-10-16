"""retrieve tweets, embedding, save into database"""

import tweepy
import basilica
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

# todo add functions later


def getLast(user):
    '''
    Gets the user and most recent tweet and loads them into the database
    '''
    twitter_user = TWITTER.get_user(user)
    timeline = twitter_user.timeline(count=10, include_rts=False,
                                     exclude_replies=True)
    user = User(name=twitter_user.screen_name, newest_tweet_id=timeline[0].id)
    tweet = Tweet(text=timeline[0].text)
    user.tweets.append(tweet)
    DB.session.add(user)
    DB.session.commit()


def reset():
    DB.drop_all()
    DB.create_all()
