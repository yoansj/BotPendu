# BotPendu

BotPendu is a hangman bot made using Twitter's API via Python, Tweepy.

## Getting Started
Firt install the prerequisites than feel free to clone this repository

## Prerequisites

[Python 2.7](https://www.python.org/downloads/)
[Tweepy API](http://docs.tweepy.org/en/3.7.0/install.html)

## Built with
* Python 2.7
* Tweepy
* Twitter's API
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
[Right here](https://github.com/yoansj/BotPendu/blob/master/LICENSE)

## Author
* Yoan Saint Juste

## Acknowledgments
* [The hangman pics](https://gist.github.com/chrishorton/8510732aa9a80a03c829b09f12e20d9c)
* [CS Dojo's vid that helped me at the beginning](https://www.youtube.com/watch?v=W0wWwglE1Vc&feature=youtu.be)
* [LucidProgramming's vid on how to stream](https://www.youtube.com/watch?v=wlnx-7cm4Gg&feature=youtu.be)
* [Tweepy's doc and it's code snippets](http://docs.tweepy.org/en/latest/getting_started.html)
* [Learnpython.org tutorials since it was my first time using Python](https://www.learnpython.org)
