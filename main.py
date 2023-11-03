from Function_List.Finance.getStockPrice import getStockPrice
from Function_List.Finance.getFinanceNews import getFinanceNews
from Function_List.Finance.Finance_autoComplete import Finance_autoComplete

from Function_List.Weather.Weather_autoComplete import Weather_autoComplete
from Function_List.Weather.getRealtimeWeather import getRealtimeWeather
from Function_List.Weather.getForecastWeather import getForecastWeather

from Function_List.Translation.Translation_detectLang import Translation_detectLang
from Function_List.Translation.Translation_translateLang import (
    Translation_translateLang,
)

from Function_List.Internet.Internet_googleSearch import Internet_googleSearch

import openai
import json
import sys
import configparser
import uuid
import os

# Load the config file
config = configparser.ConfigParser()
config.read("config.ini")

gpt_model = config["openai"]["gpt_model"]

# Import the functions


def load_api_key():
    """
    Loads the OpenAI API key from the config file.

    Parameters:
    - None

    Returns:
    - None
    """
    try:
        openai.api_key = config["openai"]["openai_api_key"]
        print("Successfully loaded the API key.")
    except Exception as e:
        print("Error: Failed to load the API key.")
        print(f"Exception: {e}")
        sys.exit(1)


def generate_message_template(role, content):
    """
    Generate a message template.

    Parameters:
    - role (str): Role of the sender, e.g., "user" or "assistant".
    - content (str): Content of the message.

    Returns:
    - dict: A dictionary representing the message template.
    """

    return {
        "role": role,
        "content": content,
    }


def generate_function_template(name, description, parameters=None, required=None):
    """
    Generate a function template.

    Parameters:
    - name (str): Name of the function.
    - description (str): Description of the function.
    - parameters (dict, optional): A dictionary of parameter properties.
    - return_type (str, optional): Return type of the function.

    Returns:
    - dict: A dictionary representing the function template.
    """
    function_template = {
        "name": name,
        "description": description,
    }

    if parameters:
        function_template["parameters"] = {
            "type": "object",
            "properties": parameters,
        }

    if required:
        function_template["required"] = (required,)

    return function_template


def get_gpt_response(prompt, messages=None):
    """
    This function takes in a prompt and returns the response from GPT-3.5

    Parameters:
    - prompt (str): The prompt to feed into the GPT model
    - messages (list, optional): A list of messages to feed into the GPT model
    - session_uuid (str, optional): A UUID to identify the session

    Returns:
    - JSON: A JSON object representing the response from GPT-3.5
    """
    # messages = [generate_message_template("user", prompt)]
    if messages is None:
        messages = [generate_message_template("user", prompt)]

    functions = [
        generate_function_template(
            "Finance_autoComplete",
            "Before calling any other financial function, always start with the Finance_autoComplete function to retrieve the performanceId for a given stock name.",
            parameters={
                "stock_name": {"type": "string", "description": "The name of a stock."}
            },
            required=["stock_name"],
        ),
        generate_function_template(
            "getFinanceNews",
            "Fetches the latest finance news for a given performanceId. Use the performanceId provided by the Finance_autoComplete function.",
            parameters={
                "performanceId": {
                    "type": "string",
                    "description": "The performanceId obtained from the Finance_autoComplete function.",
                },
                "limit": {
                    "type": "integer",
                    "description": "The number of news to return. Default number of limit is 10, unless user specifies a different number.",
                },
            },
            required=["performanceId", "limit"],
        ),
        generate_function_template(
            "getStockPrice",
            "Retrieves the latest stock prices for a given performanceId. Use the performanceId obtained from the Finance_autoComplete function.",
            parameters={
                "performanceId": {
                    "type": "string",
                    "description": "The performanceId obtained from the Finance_autoComplete function.",
                }
            },
            required=["performanceId"],
        ),
        generate_function_template(
            "Weather_autoComplete",
            "Before calling any other weather function, always start with the Weather_autoComplete function to retrieve the latitude and longitude for a given location.",
            parameters={
                "location": {
                    "type": "string",
                    "description": "The name of a location.",
                }
            },
            required=["location"],
        ),
        generate_function_template(
            "getRealtimeWeather",
            "Retrieves the latest weather information for a given latitude and longitude. Use the latitude and longitude obtained from the Weather_autoComplete function.",
            parameters={
                "lat": {
                    "type": "string",
                    "description": "The latitude of a location.",
                },
                "long": {
                    "type": "string",
                    "description": "The longitude of a location.",
                },
            },
            required=["lat", "long"],
        ),
        generate_function_template(
            "getForecastWeather",
            "Retrieves the weather forecast for a given latitude and longitude. Use the latitude and longitude obtained from the Weather_autoComplete function. The maximum number of days to forecast is 3 days, unless user specifies a different number.",
            parameters={
                "lat": {
                    "type": "string",
                    "description": "The latitude of a location.",
                },
                "long": {
                    "type": "string",
                    "description": "The longitude of a location.",
                },
                "days": {
                    "type": "integer",
                    "description": "The number of days to forecast. Maximum is 3 days, unless user specifies a different number.",
                },
            },
            required=["lat", "long", "days"],
        ),
        generate_function_template(
            "Translation_detectLang",
            "Detects the language of a given text.",
            parameters={
                "text": {
                    "type": "string",
                    "description": "The text to detect the language.",
                }
            },
            required=["text"],
        ),
        generate_function_template(
            "Translation_translateLang",
            "Translates a given text to a given language.",
            parameters={
                "text": {
                    "type": "string",
                    "description": "The text to translate.",
                },
                "target_lang": {
                    "type": "string",
                    "description": "The language to translate the text to.",
                },
                "source_lang": {
                    "type": "string",
                    "description": "The language of the text. If not specified, the language will be automatically detected.",
                },
            },
            required=["text", "target_lang"],
        ),
        generate_function_template(
            "Internet_googleSearch",
            """
            This function searches Google for a specific query and returns the top 100 results. It is essential when seeking information about current events, historical events, or other general knowledge topics.
            
            Use Cases:
            - For inquiries related to specific events or topics after July 5th, 2022, as the built-in knowledge of the assistant may not have the latest information beyond this date.
            - For comprehensive research on topics, as the function provides a wide range of top search results.
            - For accessing the most recent updates on current events or evolving situations.
            
            Note: It is recommended to utilize this function especially when the user asks questions about events or knowledge post-July 5th, 2022, to ensure the most up-to-date and accurate information is provided.
            """,
            parameters={
                "query": {
                    "type": "string",
                    "description": "The specific query or topic to search on Google.",
                },
                "limit": {
                    "type": "integer",
                    "description": "The number of results to retrieve. By default, it returns the top 100 results, but users can specify a different number if needed.",
                },
            },
            required=["query, limit"],
        ),
    ]

    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            # Finance
            "Finance_autoComplete": Finance_autoComplete,
            "getFinanceNews": getFinanceNews,
            "getStockPrice": getStockPrice,
            # Weather
            "Weather_autoComplete": Weather_autoComplete,
            "getRealtimeWeather": getRealtimeWeather,
            "getForecastWeather": getForecastWeather,
            # Translation
            "Translation_detectLang": Translation_detectLang,
            "Translation_translateLang": Translation_translateLang,
            # Internet
            "Internet_googleSearch": Internet_googleSearch,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            **function_args
        )  # call the function with the arguments

        # Step 4: send the info on the function call and function response to GPT
        # extend conversation with assistant's reply
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        second_response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=messages,
            functions=functions,
            function_call="auto",
        )  # get a new response from GPT where it can see the function response

        if response["choices"][0]["message"].get("function_call"):
            # if GPT still wants to call a function, repeat steps 2-4
            return get_gpt_response(prompt, messages)

        return json.dumps(second_response["choices"][0]["message"], indent=4)
    else:
        return json.dumps(response_message, indent=4)


def main(session_uuid=None):
    load_api_key()

    if session_uuid == "":
        session_uuid = uuid.uuid4()

    # else use the session_uuid provided by the user to get the context from sessions/{session_uuid}.json
    # if the file does not exist, create a new file with the session_uuid
    # if os.path.isfile(f"sessions/{session_uuid}.json"):
    #     with open(f"sessions/{session_uuid}.json", "r") as f:
    #         context = json.load(f)
    # else:
    #     context = {}
    
    os.makedirs("sessions", exist_ok=True)
    context = {}
    if os.path.isfile(f"sessions/{session_uuid}.json"):
        with open(f"sessions/{session_uuid}.json", "r") as f:
            context = json.load(f)
    else:
        with open(f"sessions/{session_uuid}.json", "w") as f:
            json.dump(context, f, indent=4)

    # use Internet prompt
    internet_prompt = (
        "use the Internet_googleSearch function to complete this request: "
    )
    prompt = "what is the base price of shipping from US to SG using DHL for a 0.5kg package?"
    prompt = internet_prompt + prompt
    
    # append the context to the prompt
    prompt = f"{prompt}\n\nContext: {context}"
    
    response = get_gpt_response(prompt)

    response = json.loads(response)
    
    # output the response to the session_uuid.json file
    context = response["context"]
    with open(f"sessions/{session_uuid}.json", "w") as f:
        json.dump(context, f, indent=4)

    print(response["content"])

    # delete all .pyc files in the directory and subdirectories and __pycache__ folders
    import glob
    import shutil

    for pyc_folder in glob.glob("**/__pycache__", recursive=True):
        shutil.rmtree(pyc_folder)


if __name__ == "__main__":
    session_uuid = ""
    main(session_uuid)
