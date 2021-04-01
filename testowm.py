import pyowm
import os
from dotenv import load_dotenv
from os.path import join, dirname
from google_trans_new import google_translator  

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

APIKEY = os.environ.get("API_KEY")
owm = pyowm.OWM(APIKEY)
mgr = owm.weather_manager()
mgruv = owm.uvindex_manager()
reg = owm.city_id_registry()

list_of_locations = reg.locations_for('Yellowknife', country='CA')
place = list_of_locations[0]

one_call = mgr.one_call(lat=place.lat, lon=place.lon)
uvi = mgruv.uvindex_around_coords(place.lat, place.lon)
print(uvi.to_dict()['value'])
print(one_call)
hourly = one_call.forecast_hourly
daily = one_call.forecast_daily
print(daily[0].status)
print(daily[0].detailed_status)

for x in range(len(hourly)):
    print(hourly[x].rain)

print(one_call.forecast_daily[0].temperature('celsius'))
print(one_call.current.temperature('celsius'))


observation = mgr.weather_at_place('Leiria, PT')
weather = observation.weather
print(weather.status)
print(weather.detailed_status)

translator = google_translator()  
translate_text = translator.translate(weather.detailed_status, lang_tgt='pt')  
print(translate_text)
print(weather.sunset_time(timeformat='date'))
