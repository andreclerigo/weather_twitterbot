import pycountry
import json

#To read this dictionary to a file
def write_file():
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    with open('countries.txt', 'w') as f:
        f.write(json.dumps(countries))

#To read this dictionary and save it on your code use the following function
def read_file():
    with open('countries.txt', 'r') as f:
        data = f.read()

    dict = json.loads(data)

    """
    print(dict)
    print(dict["Portugal"]) """
    return dict
