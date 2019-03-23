# Twitter-Sentiment-Analysis-WebApp

This webapp pulls twitter data, using the tweepy wrapper around the twitter API, and performs simple sentiment analysis using the vaderSentiment library. The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection. In response to URL `/realdonaldtrump` (`http://localhost/realdonaldtrump` when tested on local machine), your web server should respond with a tweet list color-coded by sentiment, using a red to green gradient:

An example URL `/realdonaldtrump` yields:

<img src=imgs/trump-tweets.png width=750>

URL to display the list of users followed by a given user, such as `/following/realdonaldtrump`:

<img src=imgs/trump-follows.png width=350>
