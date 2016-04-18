import random
import re
import sys
import twitter
from htmlentitydefs import name2codepoint as n2c
from local_settings import *
from corpus import *

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        numero = n2c[guess]
        try:
            text = unichr(numero)
        except KeyError:
            pass    
    return text

def filter_tweet(tweet):
    tweet.text = re.sub(r'\b(RT|MT) .+','',tweet.text) #take out anything after RT or MT
    tweet.text = re.sub(r'(\#|@|(h\/t)|(http))\S+','',tweet.text) #Take out URLs, hashtags, hts, etc.
    tweet.text = re.sub(r'\n','', tweet.text) #take out new lines.
    tweet.text = re.sub(r'\"|\(|\)', '', tweet.text) #take out quotes.
    htmlsents = re.findall(r'&\w+;', tweet.text)
    if len(htmlsents) > 0 :
        for item in htmlsents:
            tweet.text = re.sub(item, entity(item), tweet.text)    
    tweet.text = re.sub(r'\xe9', 'e', tweet.text) #take out accented e
    return tweet.text
                                                    
def grab_tweets(api, max_id=None):
    source_tweets=[]
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    max_id = user_tweets[len(user_tweets)-1].id-1
    for tweet in user_tweets:
        tweet.text = filter_tweet(tweet)
        if len(tweet.text) != 0:
            source_tweets.append(tweet.text)
    return source_tweets, max_id

def noart(x):
    if str.startswith(x,"!"):
        return str.lstrip(x,"!")
    return x

def art(x):
    if str.startswith(x,"!"):
        return "an " + str.lstrip(x,"!")
    return "a " + str.lstrip(x,"!")

def adj(x):
    if str.startswith(x,"$"):
        if x == "$nationality":
            return random.choice(NATIONALITY)
    return x

if __name__=="__main__":
    if DEBUG==False:
        guess = random.choice(range(ODDS))
    else:
        guess = 0

    if guess == 0:
 
        api = connect()

        x = random.randint(0,2)
        if x == 0:
            the_tweet = "The " + adj(random.choice(ADJECTIVE_STORE)) + " " + noart(random.choice(STORE_TYPE)) + " has moved to " + \
            random.choice(OTHER_NEIGHBOURHOOD) + ". In its place is a new " + \
            noart(random.choice(STORE_TYPE)) + " selling " + random.choice(ADJECTIVE_ITEM) + " " + \
            random.choice(ITEMS)
        if x == 1:
            the_tweet = "Check out the new window display at the " + adj(random.choice(ADJECTIVE_STORE)) \
            + " " + noart(random.choice(STORE_TYPE)) + ". "
            y = random.randint(0, 1)
            if y == 0:
                the_tweet += "It's " + random.choice(DISPLAY_TYPE) + " " + random.choice(NATIONALITY) + " " + noart(random.choice(ITEM))
            else:
                the_tweet += "It's " + random.choice(DISPLAY_TYPE_P) + " " + random.choice(NATIONALITY) + " " + noart(random.choice(ITEMS))
        if x == 2:
            the_tweet = "The " + random.choice(NATIONALITY) + " restaurant has been taken over by " + \
            art(random.choice(STORE_TYPE)) + ". It still sells " + random.choice(ITEMS)

        the_tweet += "."

        if str.__len__(the_tweet) < 141:
            if DEBUG == False:
                status = api.PostUpdate(the_tweet)
                print status.text.encode('utf-8')
            else:
                print the_tweet

    # Let's start up with, say, five different sentence constructions.

    # The ADJECTIVE_STORE STORE_TYPE has moved to OTHER_NEIGHBOURHOOD. In its place is a new STORE_TYPE selling ADJECTIVE_ITEM ITEM.
    # Check out the new window display at the ADJECTIVE_STORE STORE_TYPE! It's DISPLAY_TYPE NATIONALITY ITEM.
    # The NATIONALITY restaurant has been taken over by an ADJECTIVE_STORE STORE_TYPE. It still sells ITEMS.

    # Variables--
    # ADJECTIVE_STORE
    # STORE_TYPE
    # OTHER_NEIGHBOURGOOD
    # ADJECTIVE_ITEM
    # ITEM
    # NATIONALITY

    # To do:

    # Every TIME PERIOD the ADJECTIVE_STORE STORE_TYPE hosts ARTICLE + EVENT.

    # TIME PERIOD
    # EVENT
