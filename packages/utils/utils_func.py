import json
import re

def saveToJson(data_dict : dict, json_path : str):
    with open(json_path, 'r') as file:
        data = json.load(file)

    data['row'].append(data_dict)

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

def replace_within_double_curly_brackets(text):
    if text == None:
        return ""
    # Regular expression to find substrings within double curly braces
    pattern = r'{{(.*?)}}'

    # Find all matches
    matches = re.findall(pattern, text)

    # Replace each match with its last character
    for match in matches:
        last_char = match[-1] if match else ''
        text = text.replace('{{' + match + '}}', last_char)

    return text

def get_token(option : str):
    with open("./datasets/token.json", "r") as f:
        res = json.load(f)
        if option == "read":
            return res["read"]
        elif option == "write":
            return res["write"]

