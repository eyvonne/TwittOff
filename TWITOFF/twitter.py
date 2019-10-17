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


def add_or_update_user(username):
    '''Add or update a user and their tweets or else error'''
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False,
                                       tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # calulate embedding on the full tweet then truncate for storage
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('error proccessing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()
