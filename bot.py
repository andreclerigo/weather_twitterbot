import tweepy
import datetime
import time
import json
import os
from dotenv import load_dotenv
from os.path import join, dirname

def main():
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
    api = tweepy.API(auth)

    #Terminal debug
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api


#Get the last 20 mentions on the timeline
def getMention(api):
    f = open('users_accepted.txt', 'w+')
    users_accepted = [json.loads(line) for line in f]  #Do a list of dictionaries that are inside the .txt
    exists = False

    tweets = api.mentions_timeline()
    for tweet in tweets:
        handler = str(tweet.user.screen_name)
        place = str(tweet.text.replace('@WeatherBotDaily', '').strip())
        location = str(tweet.user.location)

        #Sees if the user is already in the database
        for dic in users_accepted:
            if dic.get(handler) is not None:
                exists = True

        #If the user isnt already in the databse then add him
        if not exists:
            if place == '' and location == '':
                print(handler)
                print("Dennied")
                json.dump({handler: "Dennied"}, f)
            elif place == '' and location != '':
                print(handler)
                print(location)
                json.dump({handler: location}, f)
            else:
                print(handler)
                print(place)
                json.dump({handler: place}, f)

    f.close()

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
    if now.hour == 8:
        pass
    pass


API = main()
while True:
    followBack(API)
    getMention(API)
    tweetWeather(API)
    print("Waiting..")
    time.sleep(60)