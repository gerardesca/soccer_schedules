import tweepy
import keys

BEARER_TOKEN = keys.BEARER_TOKEN
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET

def api():
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def tweet(api: tweepy.API, message: str):
    api.update_status(message)
    print('Twit')
    

def post_tweet(message):
    client = tweepy.Client(consumer_key=CONSUMER_KEY, 
                           consumer_secret=CONSUMER_SECRET, 
                           access_token=ACCESS_TOKEN, 
                           access_token_secret=ACCESS_TOKEN_SECRET)
    r = client.create_tweet(text=message)
    return r
    
    
    
#api = api()
#tweet(api, "test")
post_tweet('This was tweeted from python!!')