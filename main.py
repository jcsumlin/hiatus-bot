import os
import configparser
import praw
from datetime import datetime
import re
import random
config = configparser.ConfigParser()
config.read('auth.ini') # All my usernames and passwords for the api
# the config file is auth.ini
reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent=config.get('auth', 'reddit_user_agent'),
                     username=config.get('auth', 'reddit_username'))
bot_message = "\r\r^(I am a script. If I did something wrong, ) [^(let me know)](/message/compose/?to=J_C___&subject=all_seeing_eye_bot)"
print("Posting as: ", reddit.user.me())
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))

date_of_last_episode = datetime.strptime(config.get('auth', 'hiatus_date'), '%b %d %Y %I:%M%p')
submissions = []


if not os.path.isfile("hiatus_replied_to.txt"):
    hiatus_replied_to = []
else:
    with open("hiatus_replied_to.txt", "r") as f:
        hiatus_replied_to = f.read()
        hiatus_replied_to = hiatus_replied_to.split("\n")
        hiatus_replied_to = list(filter(None, hiatus_replied_to))


def reply_bot(hiatus_replied_to):
    subreddit = reddit.subreddit(SUBREDDIT)
    comment_stream = subreddit.stream.comments()
    for comment in comment_stream:
        if "!hiatus" in comment.body.lower() and comment.id not in hiatus_replied_to:
            days = re.search('\d{1,3}\s', str(datetime.now() - date_of_last_episode)).group(0)
            comment.reply("Days since last episode:\n\n" + "[" + days + "Days]" + bot_message)
            print("sent! \n" + comment.body)
            hiatus_replied_to.append(comment.id)
        elif "!roll" in comment.body.lower() and comment.id not in hiatus_replied_to:
            max_roll = re.search('{(\d+)}', comment.body.lower())
            if max_roll is not None:
                comment.reply(str(random.randint(1, int(max_roll.group(1)))) + bot_message)
            else:
                comment.reply(str(random.randint(1, 20)) + bot_message)
            hiatus_replied_to.append(comment.id)
            update_files(hiatus_replied_to)


def update_files(hiatus_replied_to):
    with open("hiatus_replied_to.txt", "w") as f:
        for x in hiatus_replied_to:
            f.write(x + "\n")

try:
    reply_bot(hiatus_replied_to)
except KeyboardInterrupt:
    update_files(hiatus_replied_to)
    print('Interrupted')
