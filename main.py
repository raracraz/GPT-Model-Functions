import openai
import json
import sys
import configparser

# Load the config file
config = configparser.ConfigParser()
config.read("config.ini")

gpt_model = config["openai"]["gpt_model"]

# Import the functions
from Function_List.Finance.autoComplete import autoComplete
from Function_List.Finance.getFinanceNews import getFinanceNews
from Function_List.Finance.getStockPrice import getStockPrice

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
    
def generate_function_template(name, description, parameters=None, return_type=None):
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
    
    if return_type:
        function_template["return_type"] = return_type
        
    return function_template

def get_dynamic_reaction(action, prompt, details=None):
    
    prompt_text = f"Provide an appropriate response after performing the action '{action}' with the context: {prompt}"
    
    if details:
        prompt_text += f". Additional details: {details}."

    messages = [
        {"role": "system", "content": "Your chatbot description here."}  # Use your chatbot description or keep it generic.
    ]
    messages.append({"role": "user", "content": prompt_text})
    
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        max_tokens=250
    )
    
    response_content = response.choices[0].message["content"].strip()
    print(f"get_dynamic_reaction output: {response_content}")
    return response_content

def get_gpt_response(prompt):
    messages = [generate_message_template("user", prompt)]
    
    functions = [
        generate_function_template(
            "autoComplete", 
            "Before calling any other financial function, always start with the autoComplete function to retrieve the performanceId for a given stock name.",
            parameters={"stock_name": {"type": "string"}},
            return_type={"type": "object", "properties": {"performanceId": {"type": "string"}}}
        ),
        generate_function_template(
            "getFinanceNews", 
            "Fetches the latest finance news for a given performanceId. Use the performanceId provided by the autoComplete function.",
            parameters={"performanceId": {"type": "string"}}
            
        ),
        generate_function_template(
            "getStockPrice", 
            "Retrieves the latest stock prices for a given performanceId. Use the performanceId obtained from the autoComplete function.",
            parameters={"performanceId": {"type": "string"}}
        ),
    ]

    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    
    
    
    response_message = response["choices"][0]["message"]
    
    if response_message.get("function_call"):
        available_functions = {
            "autoComplete": autoComplete,
            "getFinanceNews": getFinanceNews,
            "getStockPrice": getStockPrice,
        }
        
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)
        
        messages.append(response_message)
        
        
        # This part has been modified for chaining:
        if function_name == "autoComplete":
            performance_id = function_response
            new_message = generate_message_template("user", f"Use the performanceId {performance_id} to get me the latest finance news.")
            messages.append(new_message)
            
            # Now, you can re-query GPT-3 with the new message.
            second_response = openai.ChatCompletion.create(
                model=gpt_model,
                messages=messages,
                functions=functions,
                function_call="auto",
            )
            print(second_response)
            return second_response
        else:
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
            
            second_response = openai.ChatCompletion.create(
                model=gpt_model,
                messages=messages,
                functions=functions,
                function_call="auto",
            )
            
            return second_response
        

def main():
    load_api_key()
    prompt = "get me the latest news for Tesla"
    response = get_gpt_response(prompt)
    print(response)

if __name__ == "__main__":
    main()
