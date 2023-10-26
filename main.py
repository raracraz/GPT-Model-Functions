import openai
import json
import sys
import configparser
import os
# import the getNews function from Finance/getNews.py
from Function_List.Finance.getFinanceNews import get_finance_news

# Load the config file
config = configparser.ConfigParser()
config.read("config.ini")

def load_api_key():
    try:
        # Load the API key
        openai.api_key = config["openai"]["openai_api_key"]

        # Test the API key
        # print the model list
        print("Successfully loaded the API key.")

    except Exception as e:
        print("Error: Failed to load the API key.")
        print(f"Exception: {e}")
        sys.exit(1)

def create_message_template(role, content):
    gpt_message_template = [{
        "role": role,
        "content": content,
    }]
    return gpt_message_template

def create_function_template(name, description, parameters, return_type):
    gpt_function_template = [{
        "name": name,
        "description": description,
        "parameters": parameters,
        "return_type": return_type,
    }]
    return gpt_function_template

# Create a function to call gpt to get responses
def get_gpt_response(prompt):
    gpt_model = config["openai"]["gpt_model"]
    messages = create_message_template("user", prompt)
    functions = create_function_template("get_finance_news", "Get the latest news in finance", [], "json")

    response = openai.ChatCompletion.create(
        model = gpt_model,
        messages = messages,
        functions = functions,
        function_call = "auto",
    )
    
    response_message = response["choices"][0]["message"]
    
    if response.message.get("function_call"):
        available_functions = {
            "get_finance_news": get_finance_news,
        }
        
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)
        
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        
        second_response = openai.ChatCompletion.create(
            model = gpt_model,
            messages = messages,
        )
        
        return second_response



def main():
    # Load the API key
    load_api_key()
    
    prompt = "what is the formula for a 10 year treasury bond?"
    
    response = get_gpt_response(prompt)
    
    print(response)

if __name__ == "__main__":
    main()