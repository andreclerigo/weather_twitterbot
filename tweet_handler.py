import os
import pyowm
from dotenv import load_dotenv
from os.path import join, dirname
from generate_countries import read_file

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

#Checks if the user gave a correct country
def getTag(country):
    countries = read_file()
    
    code = ""

    try:
        code = countries[country.strip()]
    except:
        pass
    
    return code


#Checks if the user gave a correct location
def valid_location(message):
    tuple = message.strip().split(",")
    if len(tuple) != 2:
        return False, "Not valid"

    code = getTag(tuple[1])
    if code == "":
        return False, "Not valid"

    APIKEY = os.environ.get("API_KEY")
    owm = pyowm.OWM(APIKEY)
    reg = owm.city_id_registry()

    list_of_locations = reg.locations_for(tuple[0], country=code)

    if len(list_of_locations) == 0:
        return False, "Not valid"

    return True, tuple[0] + "," + tuple[1]
