import configparser
import os
import random
import re
import time
from datetime import datetime
import psutil
import praw
from loguru import logger


config = configparser.ConfigParser()
config.read('auth.ini')
try:
    reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                         client_secret=config.get('auth', 'reddit_client_secret'),
                         password=config.get('auth', 'reddit_password'),
                         user_agent='SVTFOE command bot (by u/J_C___)',
                         username=config.get('auth', 'reddit_username'))
except:
    logger.error("Reddit unable to login, check credentials in auth.ini file")

'''
Program basic static variables
'''
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))

gaged_users = ['Planckslenght', 'murrlogic', 'Dyln8R' ,'starco1984', 'Ishdd', 'StarcoFan777']


while True:
    subreddit = reddit.subreddit(SUBREDDIT)
    try:
        comment_stream = subreddit.stream.comments(pause_after=-1)
        submission_stream = subreddit.stream.submissions(pause_after=-1)
    except Exception as e:
        logger.error("Reddit stream error")
        exit()
    for comment in comment_stream:
        if comment is None:
            break
        if comment.author.name in gaged_users and not comment.approved and comment.banned_by is None:
            logger.info(comment.author.name)
            comment.mod.remove()
    for submission in submission_stream:
        if submission is None:
            break
        if submission.author.name in gaged_users and not submission.approved and submission.banned_by is None:
            logger.info(submission.author.name)
            submission.mod.remove()
