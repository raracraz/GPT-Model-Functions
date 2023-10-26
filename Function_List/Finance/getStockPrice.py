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
        "X-RapidAPI-Key": "a7ec869789mshfb612d70114af5bp1504acjsn781fc1c89727",
        "X-RapidAPI-Host": "morning-star.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())