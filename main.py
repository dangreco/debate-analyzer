import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from Tkinter import *
import Tkinter as tk
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import multiprocessing

# API KEYS
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_secret = 'ACCESS_SECRET'

# API BUILDING
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)



# CLASS TO ACTUALLY FILTER + PRINT TWEETS
class MyListener(StreamListener):


    def on_data(self, data):

        # RECORDS TRUMP DATA TO JSON
        def sentReturnT(x):
            if (x > 0):
                with open('sent.json') as fi:
                    data = json.load(fi)
                    data['trumpPos'] = data['trumpPos'] + 1
                    with open('sent.json', 'w') as out:
                        json.dump(data, out)
            if (x < 0):
                with open('sent.json') as fi:
                    data = json.load(fi)
                    data['trumpNeg'] = data['trumpNeg'] + 1
                    with open('sent.json', 'w') as out:
                        json.dump(data, out)

        # RECORDS HILLARY DATA TO JSON
        def sentReturnH(x):
            if (x > 0):
                with open('sent.json') as fi:
                    data = json.load(fi)
                    data['hillaryPos'] = data['hillaryPos'] + 1
                    with open('sent.json', 'w') as out:
                        json.dump(data, out)
            if (x < 0):
                with open('sent.json') as fi:
                    data = json.load(fi)
                    data['hillaryNeg'] = data['hillaryNeg'] + 1
                    with open('sent.json', 'w') as out:
                        json.dump(data, out)

        # MAIN CODE TO FETCH AND ANALYZE TWEETS

        dataSTR = str(data)                             # MAKES STRING OUT OF TWEET DATA
        if '"text":"' in dataSTR:                       # IF TWEET HAS ACTUAL TEXT
            start = dataSTR.index('"text":"') + 8
            dataSTR = dataSTR[start:]
            if '","source":"' in dataSTR:               # DOUBLE CHECK TO MAKE SURE THERE IS TEXT
                end = dataSTR.index('","')
                dataSTR = dataSTR[:end]
                dataSTR = dataSTR.lower()               # MAKES LOWERCASE FOR SIMPLICITY
                vs = vaderSentiment(dataSTR)
                if (not (dataSTR[0:4] == 'rt @')):      # EXCLUDES RETWEETS
                    if "hillary" in dataSTR:
                        sentReturnH(vs['compound'])
                    if "trump" in dataSTR:
                        sentReturnT(vs['compound'])

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["trump","hillary"])
