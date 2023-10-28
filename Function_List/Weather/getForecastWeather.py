import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def getForecastWeather(lat, long, days=1):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q": lat + "," + long, "days": days}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    response_json = response.json()
    forecast_data = response_json['forecast']['forecastday']
    response_json = [{"date": day["date"], "day": day["day"]} for day in forecast_data]

    return(json.dumps(response_json, indent=4))