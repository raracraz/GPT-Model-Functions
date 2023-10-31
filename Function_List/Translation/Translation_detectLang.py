import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def Translation_detectLang(text):
    
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"

    payload = { "q": text }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return(json.dumps(response.json(), indent=4))