from logging_utils import log_message
import tweepy
import keys

BEARER_TOKEN = keys.BEARER_TOKEN
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET

def client():
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def create_tweet_with_media(message: str, media):
    if media != None:
        api = client()
        api.update_status_with_media(message, media)
        log_message('INFO', "Tweet publicated successfully")
    else:
        log_message('INFO', "Tweet didnt publicated")