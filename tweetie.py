import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token,
    access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, \
        access_token, access_token_secret \
        = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of
    the Twitter user, create a list of tweets where
    each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's
              polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single
    Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    MAX_TWEETS = 100
    tweets = []
    analyser = SentimentIntensityAnalyzer()

    for t in tweepy.Cursor(api.user_timeline, id=name).items(MAX_TWEETS):
        tweet = {
            'id': t.id,
            'created': t.created_at,
            'retweeted': t.retweet_count,
            'text': t.text,
            'hashtags': [h['text'] for h in t.entities['hashtags']],
            'urls': [u['url'] for u in t.entities['urls']],
            'mentions': [m['screen_name'] for m in t.entities['user_mentions']],
            'score': analyser.polarity_scores(t.text)['compound']
        }
        tweets.append(tweet)

    # screen_name = t.user.name
    tweet_dict = {
        'user': name,
        'count': t.user.statuses_count,
        'tweets': tweets
    }

    return tweet_dict


def fetch_following(api, name):
    """
    Given a tweepy API object and the screen name
    of the Twitter user, return a a list of dictionaries
    containing the followed user info with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    followed_list = []
    for user in tweepy.Cursor(api.friends, id=name).items():
        followed_list.append({'name': user.name,
                              'screen_name': user.screen_name,
                              'followers': user.followers_count,
                              'created': user.created_at,
                              'image': user.profile_image_url
                              })

    return followed_list
