import json
import random
from collections import defaultdict
from tqdm import tqdm
import os

from packages.utils_func import get_champion_description


N_TRIPLETS_PER_PAIR = 2
input_file = f"./data/contrastive/champion_triplets.jsonl"
output_file = f"./data/contrastive/out/champion_triplets_sampled_{N_TRIPLETS_PER_PAIR}.jsonl"
output_file_1 = f"./data/contrastive/out/champion_description_triplets_sampled_1.jsonl"
output_file_2 = f"./data/contrastive/out/champion_description_triplets_sampled_2.jsonl"


# Read all triplets
triplets = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        triplet = json.loads(line)
        triplets.append(triplet)

# Group triplets by (anchor, positive)

pair_dict = defaultdict(list)
for triplet in tqdm(triplets):
    key = (triplet["anchor"], triplet["positive"])
    pair_dict[key].append(triplet)

    sampled_triplets = []
    for triplet_list in pair_dict.values():
        if len(triplet_list) <= N_TRIPLETS_PER_PAIR:
            sampled = triplet_list
        else:
            sampled = random.sample(triplet_list, N_TRIPLETS_PER_PAIR)
        sampled_triplets.append(sampled)

for triplet_group in sampled_triplets:
    for triplet in triplet_group:
        anchor_1 = get_champion_description(triplet["anchor"], "1")
        anchor_2 = get_champion_description(triplet["anchor"], "2")
        positive_1 = get_champion_description(triplet["positive"], "1")
        positive_2 = get_champion_description(triplet["positive"], "2")
        negative_1 = get_champion_description(triplet["negative"], "1")
        negative_2 = get_champion_description(triplet["negative"], "2")
        
        if anchor_1 is None or anchor_2 is None or positive_1 is None or positive_2 is None or negative_1 is None or negative_2 is None:
            continue
        
        if not(os.path.exists(output_file)):
            open_mode = "w"
        else:
            open_mode = "a"
        
        with open(output_file, open_mode) as o:
            o.write(json.dumps({
                "anchor": triplet["anchor"],
                "positive": triplet["positive"],
                "negative": triplet["negative"]
            }) + "\n")
        
        if not(os.path.exists(output_file_1)):
            open_mode = "w"
        else:
            open_mode = "a"
        
        with open(output_file_1, open_mode) as o1:
            o1.write(json.dumps({
                "anchor": anchor_1,
                "positive": positive_1,
                "negative": negative_1
            }) + "\n")
            o1.write(json.dumps({
                "anchor": anchor_1,
                "positive": positive_2,
                "negative": negative_1,
            }) + "\n")
            o1.write(json.dumps({
                "anchor": anchor_2,
                "positive": positive_1,
                "negative": negative_1
            }) + "\n")
            o1.write(json.dumps({
                "anchor": anchor_2,
                "positive": positive_2,
                "negative": negative_1
            }) + "\n")
            
        if not(os.path.exists(output_file_2)):
            open_mode = "w"
        else:
            open_mode = "a"
        with open(output_file_2, open_mode) as o2:
            o2.write(json.dumps({
                "anchor": anchor_1,
                "positive": positive_1,
                "negative": negative_2
            }) + "\n")
            o2.write(json.dumps({
                "anchor": anchor_1,
                "positive": positive_2,
                "negative": negative_2,
            }) + "\n")
            o2.write(json.dumps({
                "anchor": anchor_2,
                "positive": positive_1,
                "negative": negative_2
            }) + "\n")
            o2.write(json.dumps({
                "anchor": anchor_2,
                "positive": positive_2,
                "negative": negative_2
            }) + "\n")