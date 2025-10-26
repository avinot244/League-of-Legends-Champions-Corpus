import json
from typing import Literal
import os
from tqdm import tqdm
import time

from services.data_augmentation.augmentation.champion_triplets import champion_triplets

TRIPLET_PATH : str = "./data/contrastive/champion_triplets.jsonl"
OUT_PATH : str = "./data/contrastive/out/champion_triplets_rationales.jsonl"

# Building the triplets with the champions descriptions
def get_champion_description(champion : str, version : Literal["1", "2"]):
    with open(f"./data/fill-mask/champion_description_{version}_augmented.jsonl", "r") as f:
        for line in f.readlines():
            data : dict = json.loads(line)
            if data["label"] == champion:
                return data["text"]

with open(TRIPLET_PATH, "r") as f:
    triplets : list[dict] = [json.loads(line) for line in f.readlines()]


for idx, triplet in enumerate(tqdm(triplets[291:])):

    anchor : str = get_champion_description(triplet["anchor"], "1")
    positive : str = get_champion_description(triplet["positive"], "1")
    negative : str =  get_champion_description(triplet["negative"], "1")
    
    time.sleep(1)
    
    rationale_triplets_anthropic : list[dict] = champion_triplets(anchor, positive, negative, idx, 2, "anthropic")
    rationale_triplets_openai : list[dict] = champion_triplets(anchor, positive, negative, idx, 2, "openai")
    
    if not(os.path.exists(OUT_PATH)):
        open_mode = "w"
    else:
        open_mode = "a"
        
    if not(rationale_triplets_anthropic is None):
        with open(OUT_PATH, open_mode) as o:
            for rationale_triplet in rationale_triplets_anthropic:
                o.write(json.dumps(rationale_triplet["triplet"]) + "\n")
    
    if not(rationale_triplets_openai is None):
        with open(OUT_PATH, open_mode) as o:
            for rationale_triplet in rationale_triplets_openai:
                o.write(json.dumps(rationale_triplet["triplet"]) + "\n")
                