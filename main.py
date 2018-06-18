import configparser
import logging
import os
import random
import re
import time
from datetime import datetime
from pushbullet import Pushbullet

import coloredlogs
import praw

coloredlogs.install()


logging.basicConfig(filename='bot.log', level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

config = configparser.ConfigParser()
config.read('auth.ini')
pb = Pushbullet(str(config.get('auth', 'pb_key')))
reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent='SVTFOE command bot (by u/J_C___)',
                     username=config.get('auth', 'reddit_username'))
date_of_last_episode = datetime.strptime(config.get('auth', 'hiatus_date'), '%b %d %Y %I:%M%p')  # Set from config
logging.info("-----Starting Hiatus Bot------")
logging.info("Posting as: %s" % reddit.user.me())

'''
Program basic static variables
'''
bot_message = "\r\r^(I am a script. If I did something wrong, ) [^(let me know)](/message/compose/?to=J_C___&subject=ALERT!+Hiatus+Bot+Gone+Wild!)"
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))
bot_list = ['agree-with-you',
            'Defiantly_Not_A_Bot',
            'CommonMisspellingBot',
            'WhoaItsAFactorial',
            'FatFingerHelperBot',
            'anti-gif-bot',
            'LimbRetrieval-Bot']

turf_copy_pasta = "First, take a big step back... And literally, F-CK YOUR OWN FACE! I don't know what kind of pan-pacific bullshit power play you're trying to pull here, but r/StarVStheForcesofEvil is my territory. So whatever you're thinking, you'd better think again! Otherwise I'm gonna have to head down there and I will rain down in a Godly f-cking firestorm upon you! You're gonna have to call the f-cking United Nations and get a f-cking binding resolution to keep me from f-cking destroying you. I'm talking about a scorched earth, motherf-cker! I will massacre you! I WILL f-ck YOU UP!"
hug = ['http://i0.kym-cdn.com/photos/images/newsfeed/000/947/098/6df.gif',
       'http://i0.kym-cdn.com/photos/images/original/001/310/020/e05.gif',
       'https://78.media.tumblr.com/a673b38043cf81e7b086bb913ebd310f/tumblr_nv32cog7uR1qb7fxzo1_500.gif',
       'http://i0.kym-cdn.com/photos/images/original/000/920/953/c79.gif',
       'http://i0.kym-cdn.com/photos/images/newsfeed/001/314/915/5b1.gif',
       'https://78.media.tumblr.com/7c90bbbfd7b569c1030570ce64e0921b/tumblr_p6t0wzWyig1wlrjn3o1_500.gif',
       'https://i.pinimg.com/originals/ee/7e/92/ee7e9211b75b471bd64f88b696a6bce2.gif']


if not os.path.isfile("hiatus_replied_to.txt"):
    hiatus_replied_to = []
else:
    with open("hiatus_replied_to.txt", "r") as f:
        hiatus_replied_to = f.read()
        hiatus_replied_to = hiatus_replied_to.split("\n")
        hiatus_replied_to = list(filter(None, hiatus_replied_to))


def reply_bot():
    subreddit = reddit.subreddit(SUBREDDIT)
    comment_stream = subreddit.stream.comments()
    for comment in comment_stream:
        if "!hiatus" in comment.body.lower() and comment.id not in hiatus_replied_to:
            days = re.search('\d{1,3}\s', str(datetime.now() - date_of_last_episode)).group(0)
            comment_id = comment.reply("Days since last episode:\n\n" + "[" + days + "Days]" + bot_message)
            logging.info('Comment left successfully: ' + comment_id)
            hiatus_replied_to.append(comment.id)
            update_files(hiatus_replied_to)
        elif "!roll" in comment.body.lower() and comment.id not in hiatus_replied_to:
            max_roll = re.search('{(\d+)}', comment.body.lower())
            if max_roll is not None:
                comment.reply(str(random.randint(1, int(max_roll.group(1)))) + bot_message)
            else:
                comment.reply(str(random.randint(1, 20)) + bot_message)
            logging.info("Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.append(comment.id)
            update_files(hiatus_replied_to)
        #Turf Bot
        elif comment.author in bot_list and comment.id not in hiatus_replied_to:
            comment.reply(turf_copy_pasta)
            logging.info("Bot put in its place: %s" % comment.id)
            hiatus_replied_to.append(comment.id)
            update_files(hiatus_replied_to)
        elif "!lmgtfy" in comment.body.lower() and (comment.is_root is False) and (comment.id not in hiatus_replied_to):
            query = comment.parent().body.replace(" ", "+")
            comment.parent().reply("[Let Me Google That For You](http://lmgtfy.com/?iie=1&q=" + query + ")" + bot_message)
            logging.info("(lmgtfy) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.append(comment.id)
        elif "!hug" in comment.body.lower() and comment.is_root is False and comment.id not in hiatus_replied_to:
            comment.parent().reply(("u/%s [sent you a hug! (づ￣ ³￣)づ](" + random.choice(hug) + ")"+ bot_message) % comment.author)
            logging.info("(Hug) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.append(comment.id)
        elif "!coinflip" in comment.body.lower() and comment.id not in hiatus_replied_to:
            coin = ['Heads', 'Tails']
            comment.reply(random.choice(coin) + bot_message)
            logging.info("(CoinFlip) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.append(comment.id)




def update_files(hiatus_replied_to):
    with open("hiatus_replied_to.txt", "w") as f:
        for x in hiatus_replied_to:
            f.write(x + "\n")

if __name__ == "__main__":
    while True:
        try:
            reply_bot()
        except KeyboardInterrupt:
            print('Interrupted, files updated')
        except (AttributeError, praw.exceptions.PRAWException) as e:
            logging.warning("PRAW encountered an error, waiting 30s before trying again. %s" % e)
            time.sleep(30)
            pass
        except praw.exceptions.APIException as e:
            logging.warning("Reddit API encountered an error. %s" % e)
            pass
        except Exception as e:
            logging.critical("Uncaught error: %s" % e)
            time.sleep(30)
            pass
        finally:
            push = pb.push_note("SCRIPT Down", "J_C___ Hiatus Script is Down!")
            update_files(hiatus_replied_to)



