import tweepy
import pyowm  #import Python Open Weather Map
import datetime
import time
import json
import os
from pyowm.weatherapi25 import observation
from dotenv import load_dotenv
from os.path import join, dirname


#Get the last 20 mentions on the timeline
def getMention(api):
    with open('users_accepted.txt', 'r') as f:
        users_accepted = json.load(f)
        print(users_accepted)

    with open('users_accepted.txt', 'w') as f:
        exists = False
        data = []

        tweets = api.mentions_timeline()
        for tweet in tweets:
            handler = str(tweet.user.screen_name)
            place = str(tweet.text.replace('@WeatherBotDaily', '').strip())
            location = str(tweet.user.location)

            #Sees if the user is already in the database
            for dic in users_accepted:
                if dic.get(handler) is not None:
                    exists = True

            print(exists)
            #If the user isnt already in the databse then add him
            if not exists:
                d = {}
                if place == '' and location == '':
                    print(handler)
                    print("Dennied")
                    """ d = {handler: "Dennied"}
                    data.append(dict(d)) """
                elif place == '' and location != '':
                    d = {handler: location}
                    data.append(dict(d))
                else:
                    d = {handler: place}
                    data.append(dict(d))

        for dat in data:
            users_accepted.append(dat)
        json.dump(users_accepted, f)


#Follows everyone back
def followBack(api):
    print("\nFollowers:")
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print(follower.screen_name)
    print()


#Checks if the user 
def checkCity():
    pass


#Tweets the weather
def tweetWeather(api):
    now = datetime.datetime.now()
    if now.hour == 21:
        with open('users_accepted.txt', 'r') as f:
            users_accepted = json.load(f)  #Do a list of dictionaries that are inside the .txt
        
        for dic in users_accepted:
            key, value = list(dic.items())[0]  #Get the handler as a string
            observation = mgr.weather_at_place("Batalha, PT")
            w = observation.weather
            print(key + " vao estar " + str(w.temperature('celsius')['temp']))
    pass


#Setting up variables
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

#Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#Create API object
api = tweepy.API(auth, wait_on_rate_limit = True)

#Terminal debug
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

APIKEY = os.environ.get("API_KEY")
OpenWMap = pyowm.OWM(APIKEY)
mgr = OpenWMap.weather_manager()

while True:
    #followBack(api)
    getMention(api)
    tweetWeather(api)
    print("Waiting..")
    time.sleep(60)