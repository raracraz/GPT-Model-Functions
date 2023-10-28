import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def Weather_autoComplete(location):
    url = "https://weatherapi-com.p.rapidapi.com/search.json"

    querystring = {"q": location}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return(json.dumps(response.json(), indent=4))