import os
import json


with open("./datasets/fill-mask/lol-champs.jsonl", "r") as f:
    for line in f:
        champ_data : dict = json.load(line)
        print(champ_data)