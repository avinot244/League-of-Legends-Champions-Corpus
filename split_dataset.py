import math
import random
import json

#80% : train
#20% : validation

with open("./datasets/fill-mask/lol-champs-fused.jsonl", "r") as f:
    lines = f.readlines()
    random.shuffle(lines)
    split : int = math.floor(0.8 * len(lines))
    train_split : list[str] = lines[:split]
    validation_split : list[str] = lines[split:]
    
    
    with open("./datasets/fill-mask/lol-champs-train.jsonl", "w") as f_t:
        for line_t in train_split:
            f_t.write(json.dumps(line_t))
            f_t.write("\n")
            
    with open("./datasets/fill-mask/lol-champs-validation.jsonl", "w") as f_v:
        for line_v in validation_split:
            f_v.write(json.dumps(line_v))
            f_v.write("\n")
            
    
    