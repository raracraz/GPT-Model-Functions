import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]


def getFinanceNews(performanceId, limit=3):
    # if there is no performance id, use the default one
    if not performanceId:
        performanceId = "0P0000OQN8"

    url = "https://morning-star.p.rapidapi.com/articles/list"
    querystring = {"performanceId": performanceId}
    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "morning-star.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)

    # return only the title and Id of the news
    response_json = [{"Id": news["Id"], "Title": news["Title"]} for news in response.json()]
    
    return json.dumps(response_json, indent=4)

