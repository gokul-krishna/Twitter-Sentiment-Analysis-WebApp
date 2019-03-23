"""
A server that responds with two pages, one showing
the most recent 100 tweets for given user and the
other showing the people that follow that given user
(sorted by the number of followers those users have).

For authentication purposes, the server takes a
command-line argument that indicates the file containing
Twitter data in a CSV file format:

consumer_key, consumer_secret, access_token,
access_token_secret
"""

import sys
import os
from flask import Flask, render_template, send_from_directory
from tweetie import *
from colour import Color
from numpy import median

app = Flask(__name__)


def add_color(tweets):
    """
    Given a list of tweets, one dictionary per tweet, add
    a "color" key to each tweets dictionary with a value
    containing a color graded from red to green. Pure red
    would be for -1.0 sentiment score and pure green would
    be for sentiment score 1.0.

    Use colour.Color to get 100 color values in the range
    from red to green. Then convert the sentiment score from -1..1
    to an index from 0..100. That index gives you the color increment
    from the 100 gradients.

    This function modifies the dictionary of each tweet. It lives in
    the server script because it has to do with display not collecting
    tweets.
    """
    colors = list(Color("red").range_to(Color("green"), 100))
    for t in tweets:
        score = t['score']
        if score == 1:
            t['color'] = colors[99].hex
        else:
            t['color'] = colors[int(100 * (score + 1) / 2)].hex

    return tweets


@app.route("/favicon.ico")
def favicon():
    """
    Open and return a 16x16 or 32x32 .png or
    other image file in binary mode.
    This is the icon shown in the browser
    tab next to the title.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route("/<name>")
def tweets(name):
    """Display the tweets for a screen name
       color-coded by sentiment score"""
    tweet_dict = fetch_tweets(api, name)
    tweets = add_color(tweet_dict['tweets'])
    median_score = median([t['score'] for t in tweets])
    return render_template('tweets.html',
                           tweets=tweets,
                           name=tweet_dict['user'],
                           median_score=median_score)


@app.route("/following/<name>")
def following(name):
    """
    Display the list of users followed by a screen name,
    sorted in reverse order by the number of followers
    of those users.
    """
    followed_list = fetch_following(api, name)
    followed_list.sort(key=lambda x: x['followers'], reverse=True)
    return render_template('following.html',
                           followed=followed_list,
                           name=name)


i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i + 1]
api = authenticate(twitter_auth_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)