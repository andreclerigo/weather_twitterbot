import tweepy
import time
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

def getMention(api):
    users = []
    tweets = api.mentions_timeline()
    for tweet in tweets:
        users.append(api.get_user(tweet.user.screen_name))
        print(f"{tweet.user.name} disse {tweet.text}\n")
        print(users)

#Follows everyone back
def followBack(api):
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print(follower.screen_name)
        api.update_status(f"@{follower.screen_name} ola!")

myAPI = main()
while True:
    followBack(myAPI)
    getMention(myAPI)
    print("Waiting..")
    time.sleep(60)