import openai
import json
import sys
import configparser
import os

def load_api_key():
    try:
        # Load the config file
        config = configparser.ConfigParser()
        config.read("config.ini")

        # Load the API key
        openai.api_key = config["openai"]["api_key"]

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

def main():
    # Load the API key
    load_api_key()

if __name__ == "__main__":
    main()