import os
import time
import json
import pyowm  #import Python Open Weather Map
import tweepy
import datetime
from dotenv import load_dotenv
from os.path import join, dirname
from generate_countries import read_file
from tweet_handler import valid_location
from google_trans_new import google_translator  


#Get the last 20 mentions on the timeline and store it on a file
def getMention(api):
    tweets = api.mentions_timeline()

    with open('users_accepted.txt', 'r') as f:
        users_accepted = json.load(f)
        print(users_accepted)

    with open('users_accepted.txt', 'w') as f:
        #user_exists = False
        location_exists = False
        data = []

        for tweet in tweets:
            tag = str(tweet.user.screen_name)

            #Sees if the user is already in the database
            for dic in users_accepted:
                if dic.get(tag) is not None:
                    user_exists = True
                    break
                else:
                    user_exists = False

            #If the user isnt already in the databse then add him
            if not user_exists:
                message = str(tweet.text.replace('@BotTestWeather1', '').strip())

                location_exists, place = valid_location(message)

                if location_exists:
                    d = {tag: place}
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


#Check there will be rain in the location
def checkBadConditions(onecall):
    status = onecall.forecast_daily[0].detailed_status
    
    if "snow" in status:
        rain_info = "\nHoje vai nevar " + '\U0001F328'
        return rain_info
    elif "rain" in status:
        translator = google_translator()  
        translate_text = translator.translate(status, lang_tgt='pt') 
        rain_info = "\nHoje vai ter " + translate_text + " " + '\U0001F327'
        return rain_info
    else:
        pass


#Tweets the weather
def tweetWeather(api):
    now = datetime.datetime.now()
    if now.hour == 20:
        with open('users_accepted.txt', 'r') as f:
            users_accepted = json.load(f)  #Do a list of dictionaries that are inside the .txt
        
        countries = read_file()

        for user in users_accepted:
            key, value = list(user.items())[0]  #Get the handler as a string

            city, country = value.split(",")
            code = countries[country.strip()]
            
            place = reg.locations_for(city, code)[0]
            one_call = mgr.one_call(lat=place.lat, lon=place.lon)  #Creates a One Call object
            
            forecast = one_call.forecast_daily[0].temperature('celsius')  #Get information for the day

            tweet_content = "Dia " + str(now.day) + " de " + months[now.month-1] + " @" + key + " vai ter máximas de " + str(round(forecast['max'], 1)) + "ºC com mínimas de " + str(round(forecast['min'], 1)) + "ºC. Atualmente estão " + str(round(one_call.current.temperature('celsius')['temp'], 1)) + "ºC em " + city + ", " + code
            tweet_content += "\nA sensação de temperatura é de " + str(round(one_call.current.temperature('celsius')['feels_like'], 1)) + "ºC"

            #Bad conditions warning (rain, snow, thunder?)
            tweet_content += checkBadConditions(one_call)

            uvi = mgruv.uvindex_around_coords(place.lat, place.lon).to_dict()['value']
            tweet_content += "\nÍndice UV: " + str(round(uvi, 1))

            #Sunscreen warning
            if uvi >= 7:
                tweet_content += " mete protetor solar! " + '\U0001F9F4'

            #Beach time
            if now.month >= 5 and now.month <= 9 and forecast['max'] >= 28:
                tweet_content += "\nHoje vai estar bom para ir à praia! " + '\U0001F60E'

            #Sunset
            observation = mgr.weather_at_place(city + ", " + code)
            sunset = observation.weather.sunset_time(timeformat='date')
            tweet_content += "\nO pôr-do-sol vai ser às " + str(sunset.hour) + ":" + str(sunset.minute)

            #api.update_status(tweet_content)
            print(tweet_content)
            
            time.sleep(20)
        time.sleep(2 * 60* 60)  #Wait 2 hours


#Setting up envioment variables
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

#Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#OpenWeatherMap api setup
APIKEY = os.environ.get("API_KEY")
owm = pyowm.OWM(APIKEY)
mgr = owm.weather_manager()
mgruv = owm.uvindex_manager()
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

    #followBack(api)
    getMention(api)
    tweetWeather(api)
    print("Waiting...")
    time.sleep(2 * 60)  #Request every 2 minutes
