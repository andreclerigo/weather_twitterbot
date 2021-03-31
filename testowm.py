from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import os

APIKEY = os.environ.get("API_KEY")
owm = OWM(APIKEY)
mgr = owm.weather_manager()
reg = owm.city_id_registry()
list_of_locations = reg.locations_for('Leiria', country='PT')
place = list_of_locations[0]

one_call = mgr.one_call(lat=place.lat, lon=place.lon)

print(one_call.forecast_daily[0].temperature('celsius'))
print(one_call.current.temperature())
print(one_call.current.temperature('celsius'))