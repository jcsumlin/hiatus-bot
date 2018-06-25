import configparser
import logging
import os
import random
import re
import time
from datetime import datetime

import praw

config = configparser.ConfigParser()
config.read('auth.ini')
reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent='SVTFOE command bot (by u/J_C___)',
                     username=config.get('auth', 'reddit_username'))
print("Posting as: ", reddit.user.me())
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))


subreddit = reddit.subreddit(SUBREDDIT)
comment_stream = subreddit.stream.comments()
while True:
    for comment in comment_stream:
        if "!lmgtfy" in comment.body.lower() and comment.is_root is False:
            query = comment.parent().body.replace(" ", "+")
            comment.parent().reply("[Let Me Google That For You](http://lmgtfy.com/?iie=1&q=" + query + ")")
            logging.info("Parent Comment Replied To: %s" % comment.id)
