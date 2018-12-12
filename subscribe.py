import praw
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('auth.ini')
reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent='Watch Along reminder (by u/J_C___)',
                     username=config.get('auth', 'reddit_username'))





with open("subs.txt", "r") as f:
    users = f.read().split('\n')
date        = 'Jul 23 2018'
time        = '22:30 UTC'
time_link   = 'https://www.timeanddate.com/countdown/generic?p0=1440&iso=%sT2230' % datetime.today().strftime("%Y%m%d")
link        = 'https://www.rabb.it/J-C'
title       = 'Star vs The Forces of Evil'
imdb_link   = 'https://www.imdb.com/t2itle/tt2758770/'
disclaimer  = "^You ^are ^receiving ^this ^message ^because ^you ^indicated ^on ^the ^SVTFOE ^sub ^that ^you ^would ^like ^to ^receive ^updates ^regarding ^watch ^parties ^via ^Reddit ^mail. ^If ^you ^would ^like ^to ^unsubscribe ^please ^reply ^with ^'UNSUB' ^and ^I'll ^remove ^you ^from ^the ^list"
reddit_post = "https://www.reddit.com/r/StarVStheForcesofEvil/comments/9176rm/watch_party_round_2/"

subject = 'Watch Party Bot'
announce = ('HELLO! A watch party has been scheduled near you! You can find details [HERE](%s)! %s') % (reddit_post, disclaimer)
reminder = ('This is a reminder that the watch party is starting shortly! ([Countdown Until Event](%s)) Time to grab your popcorn and prop up your feet!\r\r Join us here : %s \r\r %s') % (time_link, link, disclaimer)
live = ("WE\'RE LIVE!!! The Watch Party will commence at 6:30 but the room is open if you wish to join early! [%s](%s)" % (link, link))
special = ("HEY YOU, YES YOU! We have a Discord server now!\r\rCome join the Watch Party After Party :D [LINK](https://discord.gg/FXfdTs)")


def send(message):
    for user in users:
        if user != "":
            try:
                reddit.redditor(user).message(subject, message)
                print('Sent to: %s' % user)
            except TypeError as e:
                print('Ran into a type error: %s' % e)
                pass
            except Exception as e:
                print('Ran into an unknown error! %s' % e)
                pass


print('------JC\'s Watch Party Program ------')
print('1. Announce Party')
print('2. Remind Peeps of party')
print('3. Remind LIVE')
print("4. Preview message")
print("5. Special Message")

option = input("Select and Option: ")
if option is "1":
    message = announce
    send(message)
elif option is "2":
    message = reminder
    send(message)
elif option is "3":
    message = live
    send(message)
elif option is "5":
    message = special
    send(message)
elif option is "4":
    option = input("Which Message Would you like to Preview? ")
    if option is "1":
        message = announce
        print(message)
    elif option is "2":
        message = reminder
        print(message)
    elif option is "3":
        message = live
        print(message)
    else:
        print("Invalid selection!")
        exit()
else:
    print("Invalid selection!")
    exit()


