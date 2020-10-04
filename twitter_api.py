import tweepy
import re


def twitter_config(key):
    credentials = open("config/twitter.config")
    found = 0
    for line in credentials:
        search = re.findall(f'{key}=(.*)',line)
        if search:
            found += 1
            return(search[0])
    if found == 0:
        return "key not found"

def twitter_post(key, secret, message):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    api.update_status(status=message)


def twitter_post_media(key, secret, message, file):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    api.update_with_media(file, status=message)


def twitter_me(key, secret):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api.me()


def twitter_posts(key, secret):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api.user_timeline()


def twitter_follow_check(key, secret):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    followers = api.followers_ids()
    retweet_users = api.friends_ids()

    # search tweets with

    # following key in returned tweets from search

    for f in retweet_users:
        if f in followers:
            print(f)
        else:
            continue


def tweet_details(key, secret, tweet_id):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api.get_status(tweet_id)


def twitter_search(key, secret, search):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api.search(search)


def twitter_isfriend(key, secret, a, b):
    consumer_key = twitter_config('consumer_key')
    consumer_secret = twitter_config('consumer_secret')
    access_token = key
    access_token_secret = secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print(api.show_friendship(source_screen_name=a, target_screen_name=b))
    return api.show_friendship(source_screen_name=a, target_screen_name=b)
