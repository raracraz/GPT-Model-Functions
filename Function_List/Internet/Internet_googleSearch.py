import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def Internet_googleSearch(query, limit=100):
    url = "https://real-time-web-search.p.rapidapi.com/search"

    querystring = {"q":query,"limit":limit}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "real-time-web-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return(json.dumps(response.json(), indent=4))