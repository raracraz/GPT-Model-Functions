import requests
import configparser

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
    
    # only return the first performance id
    # return response.json()["result"][0]["performanceId"]
    return(response.json()["results"][0]["performanceId"])