import tweepy
import pycountry
import datetime
import pyowm  #import Python Open Weather Map
import time
import json
import os
from pyowm.utils import config
from pyowm.utils import timestamps
from dotenv import load_dotenv
from os.path import join, dirname


#Get the last 20 mentions on the timeline
def getMention(api):
    tweets = api.mentions_timeline()

    with open('users_accepted.txt', 'r') as f:
        users_accepted = json.load(f)
        print(users_accepted)

    with open('users_accepted.txt', 'w') as f:
        exists = False
        data = []

        for tweet in tweets:
            handler = str(tweet.user.screen_name)
            place = str(tweet.text.replace('@BotTestWeather1', '').strip())
            location = str(tweet.user.location)

            #Sees if the user is already in the database
            for dic in users_accepted:
                if dic.get(handler) is not None:
                    exists = True

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
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
    pass


#Tweets the weather
def tweetWeather(api):
    now = datetime.datetime.now()
    if now.hour == 11:
        with open('users_accepted.txt', 'r') as f:
            users_accepted = json.load(f)  #Do a list of dictionaries that are inside the .txt
        
        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha_2

        for dic in users_accepted:
            key, value = list(dic.items())[0]  #Get the handler as a string

            city, country = value.split(",")
            code = countries[country.strip()]
            
            list_of_locations = reg.locations_for(city, country=code)
            place = list_of_locations[0]
            one_call = mgr.one_call(lat=place.lat, lon=place.lon)

            daily = one_call.forecast_daily[0].temperature('celsius')
            api.update_status("Dia " + str(now.day) + " de " + months[now.month-1] + " @" + key + " vai ter máximas de " +
                                        str(daily['max']) + "ºC com minimas de " +
                                        str(daily['min']) + "ºC. A temperatura atual é de " +
                                        str(one_call.current.temperature('celsius')['temp']) + " em " + city + ", " + code)

        time.sleep(2 * 60* 60)  #Wait 2 hours


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

APIKEY = os.environ.get("API_KEY")
owm = pyowm.OWM(APIKEY)
mgr = owm.weather_manager()
reg = owm.city_id_registry()

months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

while True:
    #Create API object
    api = tweepy.API(auth, wait_on_rate_limit = True)

    #Terminal debug
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    #print(api.rate_limit_status())
    #followBack(api)
    getMention(api)
    tweetWeather(api)
    print("Waiting...")
    time.sleep(90)