import json
from typing import Literal
import os
from tqdm import tqdm
import time

from services.data_augmentation.augmentation.champion_triplets import champion_triplets
import asyncio
from functools import partial

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

visited_champs : list[str] = []

for idx, triplet in enumerate(tqdm(triplets[2350:])):
    anchor_v1 : str = get_champion_description(triplet["anchor"], "1")
    positive_v1 : str = get_champion_description(triplet["positive"], "1")
    negative_v1 : str =  get_champion_description(triplet["negative"], "1")
    anchor_v2 : str = get_champion_description(triplet["anchor"], "2")
    positive_v2 : str = get_champion_description(triplet["positive"], "2")
    negative_v2 : str =  get_champion_description(triplet["negative"], "2")
    
    time.sleep(1)
    try:
        if not(os.path.exists(OUT_PATH)):
            open_mode = "w"
        else:
            open_mode = "a"
        # # Create async event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run both API calls concurrently and wait for results
        results = loop.run_until_complete(asyncio.gather(
            loop.run_in_executor(None, partial(champion_triplets, anchor_v1, positive_v1, negative_v1, idx, 2, "openai", model_name="gpt-4o-mini")),
            loop.run_in_executor(None, partial(champion_triplets, anchor_v1, positive_v1, negative_v1, idx, 2, "openai"))
        ))        
        
        
        rationale_triplets_anthropic, rationale_triplets_openai = results

        # rationale_triplets_openai = champion_triplets(anchor_v1, positive_v1, negative_v1, idx, 2, "openai")

        if not(rationale_triplets_anthropic is None):
            with open(OUT_PATH, open_mode) as o:
                for rationale_triplet in rationale_triplets_anthropic:
                    o.write(json.dumps(rationale_triplet["triplet"]) + "\n")
        
        if not(rationale_triplets_openai is None):
            with open(OUT_PATH, open_mode) as o:
                for rationale_triplet in rationale_triplets_openai:
                    o.write(json.dumps(rationale_triplet["triplet"]) + "\n")
                    
        # with open(OUT_PATH, open_mode) as o:
        #     if triplet["anchor"] not in visited_champs or triplet["positive"] not in visited_champs or triplet["negative"] not in visited_champs:
        #         if idx % 2 == 0:
        #             o.write(json.dumps({"anchor": anchor_v1, "positive": positive_v1, "negative": negative_v1}) + "\n")
        #         else:
        #             o.write(json.dumps({"anchor": anchor_v2, "positive": positive_v2, "negative": negative_v2}) + "\n")
        #         # Add champions to visited list after writing
        #         visited_champs.extend([triplet["anchor"], triplet["positive"], triplet["negative"]])

        loop.close()
    except Exception as e:
        print(e)
        print(f"Skipping triplet {idx}")
        continue