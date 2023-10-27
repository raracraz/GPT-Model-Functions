import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def autoComplete(stock_name):

    url = "https://morning-star.p.rapidapi.com/market/v2/auto-complete"

    querystring = {"q":stock_name}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "morning-star.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return(json.dumps(response.json(), indent=4))

if __name__ == "__main__":
    autoComplete("Tesla Inc")