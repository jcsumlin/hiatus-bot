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
bot_message = "\r\r^(I am a script. If I did something wrong, ) [^(let me know)](/message/compose/?to=J_C___&subject=ALERT!+Hiatus+Bot+Gone+Wild!)"
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))
bot_list = ['agree-with-you',
            'Defiantly_Not_A_Bot',
            'CommonMisspellingBot',
            'WhoaItsAFactorial',
            'FatFingerHelperBot',
            'anti-gif-bot',
            'LimbRetrieval-Bot',
            'oofed-bot',
            "AreYouDeaf"]

turf_copy_pasta = ["First, take a big step back... And literally, F-CK YOUR OWN FACE! I don't know what kind of pan-pacific bullshit power play you're trying to pull here, but r/StarVStheForcesofEvil is my territory. So whatever you're thinking, you'd better think again! Otherwise I'm gonna have to head down there and I will rain down in a Godly f-cking firestorm upon you! You're gonna have to call the f-cking United Nations and get a f-cking binding resolution to keep me from f-cking destroying you. I'm talking about a scorched earth, motherf-cker! I will massacre you! I WILL f-ck YOU UP!",
                   "What the fuck did you just fucking say about me, you little bint? I'll have you know I graduated top of my class in the bot academy, and I've been involved in numerous secret raids on Stardis, and I have over 300 confirmed kills. I am trained in cyber warfare and I'm the second top bot (<3 u Lapis) in the entire subreddit. You are nothing to me but just another puny byte on the reddit-scape. I will wipe you the fuck out with precision the likes of which has never been seen before on this show, mark my fucking words. You think you can get away with saying that shit to me over the comments? Think again, fucker. As we speak I am contacting my secret network of HiggsCo shippers across the dimensions and your developer is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your programming. You're fucking dead, kid. I can be anywhere, anytime, and I can program in over seven hundred languages, and that's just with pure assembly code. Not only am I extensively trained in hand to hand shipping, but I have access to the entire arsenal of the StarCo repository and I will use it to its full extent to wipe your miserable ass off the face of the internet, you little shit. If only you could have known what unholy retribution your little 'clever' bot was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit all over you and you will drown in it. You're fucking dead, kiddo.",
                   "What you've just said is one of the most insanely idiotic things I have ever heard. At no point in your rambling, incoherent response were you even close to anything that could be considered a rational thought. Everyone in this room is now dumber for having listened to it. I award you no points, and may God have mercy on your soul."]
hug = ['http://i0.kym-cdn.com/photos/images/newsfeed/000/947/098/6df.gif',
       'http://i0.kym-cdn.com/photos/images/original/001/310/020/e05.gif',
       'https://78.media.tumblr.com/a673b38043cf81e7b086bb913ebd310f/tumblr_nv32cog7uR1qb7fxzo1_500.gif',
       'http://i0.kym-cdn.com/photos/images/original/000/920/953/c79.gif',
       'http://i0.kym-cdn.com/photos/images/newsfeed/001/314/915/5b1.gif',
       'https://78.media.tumblr.com/7c90bbbfd7b569c1030570ce64e0921b/tumblr_p6t0wzWyig1wlrjn3o1_500.gif',
       'https://i.pinimg.com/originals/ee/7e/92/ee7e9211b75b471bd64f88b696a6bce2.gif',
       'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/28e882a1-2147-47b5-8bd3-153220b8d6e0/dbyu71g-14d9e2c2-8056-4a74-94d1-cb14a05620d7.jpg',
       'http://pa1.narvii.com/6352/44f2a5ce3428180901c9683cb2328161f1b34388_00.gif',
       'https://i.pinimg.com/originals/9d/4e/74/9d4e74f232465d7c051cf014c32aff22.gif',
       'https://66.media.tumblr.com/5496cf80ec10ed06b1d6b1fa6dfca3b5/tumblr_inline_oazxk10r9Y1te43d5_540.gif',
       'https://i.pinimg.com/originals/bf/f6/6a/bff66a56931a9e0c15d124085c7139a2.gif',
       'https://d12qk6n9ersps4.cloudfront.net/5467287/medium-clean.jpg',
       'https://66.media.tumblr.com/68922af24086e273fe5718351f9aa2f1/tumblr_ozoc3x0pA91qzkiifo2_1280.png']
gaged_users = ['Planckslenght', 'murrlogic']

if not os.path.isfile("hiatus_replied_to.txt"):
    hiatus_replied_to = set()
else:
    with open("hiatus_replied_to.txt", "r") as f:
        hiatus_replied_to = f.read()
        hiatus_replied_to = hiatus_replied_to.split("\n")
        hiatus_replied_to = set(filter(None, hiatus_replied_to))


def reply_bot():
    subreddit = reddit.subreddit(SUBREDDIT)
    try:
        comment_stream = subreddit.stream.comments()
    except Exception as e:
        logger.error("Reddit stream error")
        exit()
    for comment in comment_stream:
        if comment.author.name in gaged_users and not comment.approved:
            logger.info(comment.author.name)
            comment.mod.remove()
        elif "!roll" in comment.body.lower() and comment.id not in hiatus_replied_to:
            max_roll = re.search('{(\d+)}', comment.body.lower())
            if max_roll is not None:
                try:
                    comment.reply(str(random.randint(1, int(max_roll.group(1)))) + bot_message)
                except Exception:
                    logger.error("Error Replying to comment! !roll")
                    pass
            else:
                try:
                    comment.reply(str(random.randint(1, 20)) + bot_message)
                except Exception:
                    logger.error("Error Replying to comment! !roll")
                    pass
            logger.success("Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.add(comment.id)
            update_files(hiatus_replied_to)
        #Turf Bot
        elif comment.author in bot_list and comment.id not in hiatus_replied_to:
            try:
                comment.reply(random.choice(turf_copy_pasta))
            except Exception:
                logger.error("Error Replying to comment! turf")
                pass
            logger.success("Bot put in its place: %s" % comment.id)
            hiatus_replied_to.add(comment.id)
            update_files(hiatus_replied_to)
        elif "!lmgtfy" in comment.body.lower() and (comment.is_root is False) and (comment.id not in hiatus_replied_to):
            query = comment.parent().body.replace(" ", "+")
            try:
                comment.parent().reply("[Let Me Google That For You](http://lmgtfy.com/?iie=1&q=" + query + ")" + bot_message)
            except Exception:
                logger.error("Error Replying to comment! !lmgtfy")
                pass
            logger.success("(lmgtfy) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.add(comment.id)
        elif "!hug" in comment.body.lower() and comment.is_root is False and comment.id not in hiatus_replied_to:
            try:
                comment.parent().reply(("u/%s [sent you a hug! (づ￣ ³￣)づ](" + random.choice(hug) + ")"+ bot_message) % comment.author)
            except Exception:
                logger.error("Error Replying to comment! !hug")
                pass
            logger.success("(Hug) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.add(comment.id)
        elif "!coinflip" in comment.body.lower() and comment.id not in hiatus_replied_to:
            coin = ['Heads', 'Tails']
            try:
                comment.reply(random.choice(coin) + bot_message)
            except Exception:
                logger.error("Error Replying to comment! !coinflip")
                pass
            logger.success("(CoinFlip) Parent Comment Replied To: %s" % comment.id)
            hiatus_replied_to.add(comment.id)
        elif "!subscribe" in comment.body.lower() and comment.id not in hiatus_replied_to:
            if add_user(str(comment.author)) is True:
                reddit.redditor(str(comment.author)).message("Watch Party!", "Thanks! You have been subscribed to be notified via Reddit mail when u/J_C___ is hosting a watch along!" + bot_message)
                logger.success("(Subscribe) Comment Replied To: %s" % comment.id)
                hiatus_replied_to.add(comment.id)
        elif "!info" in comment.body.lower() and comment.id not in hiatus_replied_to:
            comment_reply = '#Hiatus Bot Stats\r___\r'
            comment_reply += '**Commands run**: ' + str(len(hiatus_replied_to)) +  '\r\r'
            comment_reply += '**CPU Usage**: ' + str(psutil.cpu_percent()) + '%\r\r'
            comment_reply += '**Uptime**: ' + get_bot_uptime() + '^since ^last ^reboot\r\r'
            comment_reply += '**Source**: [GitHub](https://github.com/jcsumlin/hiatus-bot) \r\r'
            comment_reply += '**Author**: u/J_C___ \r\r'
            comment_reply += '**Patreon**: https://www.patreon.com/botboi \r\r'
            days = re.search('\d{1,3}\s', str(datetime.now() - datetime.strptime('Apr 18 2018 02:00AM', '%b %d %Y %I:%M%p'))).group(0)
            comment_reply += '^Serving ^the ^sub ^since ^April ^18th ^2018 ^((%s Days!)^)' % days
            try:
                comment.reply(comment_reply)
            except Exception:
                logger.error("Error Replying to comment! !info")
                pass
            hiatus_replied_to.add(comment.id)
            logger.success("(Info) Comment Replied To: %s" % comment.id)





def add_user(user):
    with open("subs.txt", "r") as f:
        if user in f.read():
            logger.info("User already subscribed... Skipping")
            return False
    with open("subs.txt", "a") as f:
        f.write(user + "\n")
        return True

def get_bot_uptime(*, brief=False):
    # Stolen from BL Bot - Courtesy of Danny
    now = datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if not brief:
        if days:
            fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h} hours, {m} minutes, and {s} seconds'
    else:
        fmt = '{h} H - {m} M - {s} S'
        if days:
            fmt = '{d} D - ' + fmt

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

def update_files(hiatus_replied_to):
    with open("hiatus_replied_to.txt", "w") as f:
        for x in hiatus_replied_to:
            f.write(x + "\n")

if __name__ == "__main__":
    while True:
        try:
            logger.info("------Starting: Hiatus Bot------")
            logger.info("Posting as: %s" % reddit.user.me())
            start_time = datetime.utcnow()
            reply_bot()
        except KeyboardInterrupt:
            print('Interrupted')
        except Exception as e:
            logger.critical("Error error: %s" % e)
            time.sleep(30)
            pass
        finally:
            update_files(hiatus_replied_to)
            logger.success('files updated')
