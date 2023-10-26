import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def getStockPrice(performance_id):
    # if there is no performance id, use the default one
    # if not performance_id:
    #     performance_id = "0P0000OQN8"
    
    url = "https://morning-star.p.rapidapi.com/stock/v2/get-realtime-data"
    
    querystring = {"performanceId": performance_id}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "morning-star.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())