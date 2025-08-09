import json
from typing import Literal
import os
from tqdm import tqdm
import time

from services.data_augmentation.augmentation.champion_triplets import champion_triplets

# Building the triplets with the champions descriptions
def get_champion_description(champion : str, version : Literal["1", "2"]):
    with open(f"./data/fill-mask/champion_description_{version}_augmented.jsonl", "r") as f:
        for line in f.readlines():
            data : dict = json.loads(line)
            if data["label"] == champion:
                return data["text"]

with open("./data/contrastive/out/champion_triplets_sampled_2.jsonl", "r") as f:
    triplets : list[dict] = [json.loads(line) for line in f.readlines()]


for idx, triplet in enumerate(tqdm(triplets[2345:])):

    anchor : str = get_champion_description(triplet["anchor"], "1")
    positive : str = get_champion_description(triplet["positive"], "1")
    negative : str =  get_champion_description(triplet["negative"], "1")
    
    time.sleep(1)
    rationale_triplets : list[dict] = champion_triplets(anchor, positive, negative, idx, 2)
    
    if not(os.path.exists("./data/contrastive/out/champion_triplets_rationales.jsonl")):
        open_mode = "w"
    else:
        open_mode = "a"
        
    if not(rationale_triplets is None):
        with open("./data/contrastive/out/champion_triplets_rationales.jsonl", open_mode) as o:
            for rationale_triplet in rationale_triplets:
                o.write(json.dumps(rationale_triplet["triplet"]) + "\n")
                