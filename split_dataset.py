import math
import random
import json

#80% : train
#20% : validation

with open("./data/fill-mask/v6/lol-champs.jsonl", "r") as f:
    lines = f.readlines()
    random.shuffle(lines)
    split : int = math.floor(0.8 * len(lines))
    train_split : list[str] = lines[:split]
    validation_split : list[str] = lines[split:]
    
    
    with open("./data/fill-mask/v6/lol-champs-train.jsonl", "w") as f_t:
        for line_t in train_split:
            f_t.write(line_t)
            
    with open("./data/fill-mask/v6/lol-champs-validation.jsonl", "w") as f_v:
        for line_v in validation_split:
            f_v.write(line_v)
            