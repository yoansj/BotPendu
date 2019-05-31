# BotPendu

BotPendu is a hangman bot made using Twitter's API via Python, Tweepy.

## Getting Started
Firt install the prerequisites than feel free to clone this repository

## Prerequisites

[Python 2.7](https://www.python.org/downloads/)
[Tweepy API](http://docs.tweepy.org/en/3.7.0/install.html)

## Built with
> Python 2.7
> Tweepy
> Twitter's API
## How to use

Fill the keys with your Twitter app keys
```python
CONSUMER_KEY = 'REPLACE'
CONSUMER_SECRET = 'THESE'
ACCESS_KEY = 'KEYS'
ACCESS_SECRET = '(OR IT WONT WORK)'
```
[If you haven't created an app yet](https://developer.twitter.com/)

Also change this line to the tweets you want to track
```python
bot.filter(track=['fortnite'])
```
Go to the repository and use
```bash
python2.7 bot.py
```
## License
