# Create prompt to assign champions to its modality
# Update champion_mapping.json
import json
import os
from tqdm import tqdm
from typing import Dict, Tuple
from datasets import load_dataset

from services.data_augmentation.champion_feature.champion_features import generate_champion_features
from packages.utils_func import get_champion_description

def update_champion_feature():
    """update ./data/champion_mapping.json with prompt"""
    with open("./data/champion_mapping.json", "r") as f:
        data : list[dict] = json.load(f)
    
    
    for champion_metadata in tqdm(data):
        champion_description : str = get_champion_description(champion_metadata["name"])
        champion_features : dict = generate_champion_features(champion_description)
        
        if not(champion_features is None):
            for k, v in champion_features.items():
                champion_metadata[k] = v
            
            if not(os.path.exists("./data/champion_mapping_rich.jsonl")):
                open_mode : str = "w"
            else:
                open_mode : str = "a"
                
            with open("./data/champion_mapping_rich.jsonl", open_mode) as o:
                o.write(json.dumps(champion_metadata) + "\n")

def get_feature_overlap(champion_metadata_1 : Dict[str, list], champion_metadata_2 : Dict[str, list], feature_list : list[str]) -> int:
    def list_overlap(l1 : list, l2 : list) -> int:
        overlap : int = 0
        for e1 in l1:
            for e2 in l2:
                if e1 == e2:
                    overlap += 1
                    
        return overlap
    
    overlap_score : int = 0
       
    for feature in feature_list:
        try:
            if list_overlap(champion_metadata_1[feature], champion_metadata_2[feature]) > 0:
                overlap_score += 1
        except KeyError as e:
            print(list(champion_metadata_1.keys()))
            print(list(champion_metadata_2.keys()))
            raise e
    return overlap_score
    
def get_champion_metadata(champion : str, data : list[dict]):
    for d in data:
        if d["name"] == champion:
            return d

def generate_triplets(champion_metadata : list[Dict[str, list[str]]], criterion : int, output_path : str) -> list[Tuple[str, str, str]]:
    champion_list : list[str] = [d["name"] for d in champion_metadata]
    champion_synergies : Dict[str, list] = {champion:[] for champion in champion_list}
    feature_list : list[str] = ["damage_profile", "mobility", "team_role", "synergy_profile", "engage_potential", "peel_capability", "objective_control", "roaming_power"]
    
    print("Creating the synergy matrix")
    for anchor in tqdm(champion_list):
        for potential_positive in champion_list:
            if anchor != potential_positive:
                a_data = get_champion_metadata(anchor, champion_metadata)
                p_data = get_champion_metadata(potential_positive, champion_metadata)
                
                if get_feature_overlap(a_data, p_data, feature_list) >= criterion:
                    champion_synergies[anchor].append(potential_positive)
    
    with open("./temp.json", "w") as f:
        json.dump(champion_synergies, f, indent=4)
    
    print("Building the triplets")
    for anchor in tqdm(champion_list):
        visited = []
        positive_list : list[str] = champion_synergies[anchor]
        for positive in positive_list:
            negative : str = ""
            if len(visited) == 170 - len(positive_list):
                visited = []

            # Build the potential negative_list and add (anchor, positive, negative_i) for negative_i in negative_list
            for potential_negative in champion_list:
                if not(potential_negative in positive_list) and not(potential_negative in visited) and negative != positive and negative != anchor:
                    negative = potential_negative
                    visited.append(negative)
                    break
            
            if not(os.path.exists(output_path)):
                open_mode : str = "w"
            else:
                open_mode : str = "a"
            
            with open(output_path, open_mode) as o:
                o.write(json.dumps({"anchor": anchor, "positive": positive, "negative": negative}) + "\n") 
                

def generate_triplet_dataset():
    if not(os.path.exists("./data/champion_mapping_rich.jsonl")):
        update_champion_feature()
    
    with open("./data/champion_mapping_rich.jsonl", "r") as f:
        data : list[dict] = [json.loads(line) for line in f.readlines()]
    
    if len(data) < 170:
        update_champion_feature()
    
    generate_triplets(data, 8, "./data/contrastive/champion_triplets.jsonl")
    