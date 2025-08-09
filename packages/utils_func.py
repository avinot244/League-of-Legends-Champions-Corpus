import json
import re
from typing import Literal

def saveToJson(data_dict : dict, json_path : str):
    with open(json_path, 'r') as file:
        data = json.load(file)

    data['row'].append(data_dict)

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

def replace_within_double_curly_brackets(text : str) -> str:
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

def get_token(option : Literal["read", "write"], api_type : Literal["firecrawl", "huggingface", "youtube", "anthropic", "anthorpic2"]):
    with open(f"./data/tokens/tokens.json", "r") as f:
        res = json.load(f)
    
    return res[api_type][option]

def get_champion_description(champion_name : str, version : Literal["1", "2"]) -> str:
    with open(f"./data/fill-mask/champion_description_{version}.jsonl", "r") as f:
        lines = f.readlines()
        
    for line in lines:
        data = json.loads(line)
        if data["label"] == champion_name:
            return data["text"]
        
    print(f"Champion {champion_name} not found in champion_description_{version}.jsonl")