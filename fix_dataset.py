import os
import json


with open("./datasets/fill-mask/lol-champs.jsonl", "r") as f:
    i : int = 0
    j : int = 2
    
    data : list[dict] = list()
    
    for line in f:
        data.append(json.loads(line))
    
    while i < len(data) and j < len(data):
        
        line_1 : dict = data[i]
        line_2 : dict = data[j]
        
        if line_1["label"] == line_2["label"]:
            champ_data : dict = {
                "label": line_1["label"],
                "text": line_1["text"] + " " + line_2["text"]
            }
            with open("./datasets/fill-mask/lol-champs-fused.jsonl", "a") as o:
                json.dump(champ_data, o)
                o.write("\n")
        else:
            with open("./datasets/fill-mask/lol-champs-fused.jsonl", "a") as o:
                json.dump(line_1, o)
                o.write("\n")
                json.dump(line_2, o)
                o.write("\n")
        
        i += 2
        j += 2