import pyowm
from pyowm.owm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import os

from pyowm.weatherapi25 import forecast

APIKEY = "c548bc34f606696689b7c67ce8cbdbc7"
owm = pyowm.OWM(APIKEY)
mgr = owm.weather_manager()
mgruv = owm.uvindex_manager()
reg = owm.city_id_registry()

list_of_locations = reg.locations_for('Leiria', country='PT')
place = list_of_locations[0]

one_call = mgr.one_call(lat=place.lat, lon=place.lon)
uvi = mgruv.uvindex_around_coords(place.lat, place.lon)
print(uvi.to_dict()['value'])

hourly = one_call.forecast_hourly
daily = one_call.forecast_daily
print(daily[0].rain)

for x in range(len(hourly)):
    print(hourly[x].temperature('celsius').get('temp', None))

print(one_call.forecast_daily[0].temperature('celsius'))
print(one_call.current.temperature('celsius'))

observation = mgr.weather_at_place('Leiria, PT')
weather = observation.weather
print(weather.sunset_time(timeformat='date'))
