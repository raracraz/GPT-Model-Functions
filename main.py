from Function_List.Finance.getStockPrice import getStockPrice
from Function_List.Finance.getFinanceNews import getFinanceNews
from Function_List.Finance.autoComplete import autoComplete
import openai
import json
import sys
import configparser

# Load the config file
config = configparser.ConfigParser()
config.read("config.ini")

gpt_model = config["openai"]["gpt_model"]

# Import the functions


def load_api_key():
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
    # messages = [generate_message_template("user", prompt)]
    if messages is None:
        messages = [generate_message_template("user", prompt)]

    functions = [
        generate_function_template(
            "autoComplete",
            "Before calling any other financial function, always start with the autoComplete function to retrieve the performanceId for a given stock name.",
            parameters={
                "stock_name": {"type": "string", "description": "The name of a stock."}
            },
            required=["stock_name"],
        ),
        generate_function_template(
            "getFinanceNews",
            "Fetches the latest finance news for a given performanceId. Use the performanceId provided by the autoComplete function.",
            parameters={
                "performanceId": {
                    "type": "string",
                    "description": "The performanceId obtained from the autoComplete function.",
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
            "Retrieves the latest stock prices for a given performanceId. Use the performanceId obtained from the autoComplete function.",
            parameters={
                "performanceId": {
                    "type": "string",
                    "description": "The performanceId obtained from the autoComplete function.",
                }
            },
            required=["performanceId"],
        ),
    ]

    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    # response_content = response["choices"][0]["message"]["content"]
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "autoComplete": autoComplete,
            "getFinanceNews": getFinanceNews,
            "getStockPrice": getStockPrice,
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
        
        # print(json.dumps(messages, indent=4))
        
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
        
        # print(json.dumps(response_message, indent=4))
        return json.dumps(response_message, indent=4)


def main():
    load_api_key()
    prompt = "who is the president of the united states in 2004?"
    response = get_gpt_response(prompt)
    print(response)
    
    # delete all .pyc files in the directory and subdirectories and __pycache__ folders
    import glob
    import shutil
    for pyc_folder in glob.glob("**/__pycache__", recursive=True):
        shutil.rmtree(pyc_folder)

if __name__ == "__main__":
    main()