import requests
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

rapidapi_api_key = config["rapidapi"]["rapidapi_api_key"]

def getFinanceNews(performanceId): 
    
    # if there is no performance id, use the default one
	if not performanceId:
		performanceId = "0P0000OQN8"
	print(performanceId)
    
	url = "https://morning-star.p.rapidapi.com/articles/list"
	querystring = {"performanceId": performanceId}
	headers = {
		"X-RapidAPI-Key": rapidapi_api_key,
		"X-RapidAPI-Host": "morning-star.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	print(response)

	return json.dumps(response)

if __name__ == "__main__":
	getFinanceNews("0P0000OQN8")
