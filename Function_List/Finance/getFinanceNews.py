import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]


def get_news():
	url = "https://morning-star.p.rapidapi.com/articles/list"
	querystring = {"performanceId":"0P0000OQN8"}
	headers = {
		"X-RapidAPI-Key": rapidapi_api_key,
		"X-RapidAPI-Host": "morning-star.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)

	return response.json()
