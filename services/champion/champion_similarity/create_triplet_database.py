# Create prompt to assign champions to its modality
# Update champion_mapping.json
import json
import os
from tqdm import tqdm
from typing import Dict, Tuple
from datasets import load_dataset
import networkx as nx
import random

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

def jaccard_index(champion_metadata_1 : Dict[str, list], champion_metadata_2 : Dict[str, list], feature_list : list[str]) -> int:
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
    
    jaccard_score : int = overlap_score/len(feature_list)
    return jaccard_score
    
def get_champion_metadata(champion : str, data : list[dict]):
    for d in data:
        if d["name"] == champion:
            return d

def generate_pairs(champion_metadata : list[Dict[str, list[str]]], criterion : int, output_path : str, feature_list : list[str]) -> list[Tuple[str, str, str]]:
    champion_list : list[str] = [d["name"] for d in champion_metadata]
    champion_synergies : Dict[str, list[tuple]] = {champion:[] for champion in champion_list}
    
    print("Creating the synergy matrix")
    for anchor in tqdm(champion_list):
        for potential_positive in champion_list:
            if anchor != potential_positive:
                a_data = get_champion_metadata(anchor, champion_metadata)
                p_data = get_champion_metadata(potential_positive, champion_metadata)
                
                jaccard_score : int = jaccard_index(a_data, p_data, feature_list)
                
                if jaccard_score >= criterion:
                    champion_synergies[anchor].append((potential_positive, jaccard_score))
    
    with open("./temp.json", "w") as f:
        json.dump(champion_synergies, f, indent=4)
    
    print("Building the pairs")
    visited = []
    first = True
    for anchor in tqdm(champion_list):
        positive_list : list[str] = champion_synergies[anchor]
        for positive in positive_list:
            if not((anchor, positive[0]) in visited or (positive[0], anchor) in visited):
                if not(os.path.exists(output_path)) or first:
                    open_mode : str = "w"
                    first = False
                else:
                    open_mode : str = "a"
                
                with open(output_path, open_mode) as o:
                    o.write(json.dumps({"anchor": anchor, "positive": positive[0]}) + "\n")
                
                visited.append((anchor, positive[0]))
                visited.append((positive[0], anchor))
                
    return champion_synergies
                

def generate_pair_dataset():
    if not(os.path.exists("./data/champion_mapping_rich.jsonl")):
        update_champion_feature()
    
    with open("./data/champion_mapping_rich.jsonl", "r") as f:
        data : list[dict] = [json.loads(line) for line in f.readlines()]

    feature_list : list[str] = ["classes", "roles"]
    # feature_list : list[str] = ["damage_profile", "range", "mobility", "cc_profile", "team_role", "synergy_profile", "power_curve", "engage_potential", "peel_capability", "wave_clear", "objective_control", "zone_control", "roaming_power", "duel_power"]
    
    generate_pairs(data, 0.9, "./data/contrastive/champion_pairs.jsonl", feature_list)
    

def generate_triplet_dataset():
    assert os.path.exists("./data/contrastive/champion_pairs.jsonl"), "Please generate pair dataset first"
    
    with open("./data/contrastive/champion_pairs.jsonl", "r") as f:
        champion_pairs : list[dict] = [json.loads(line) for line in f.readlines()]
    
    # Building the list of champions
    champion_list : list[str] = list()
    for pair in champion_pairs:
        if not(pair["anchor"] in champion_list):
            champion_list.append(pair["anchor"])
        if not(pair["positive"] in champion_list):
            champion_list.append(pair["positive"])
    
    # Building the graph using networkx
    G = nx.Graph()
    for pair in champion_pairs:
        G.add_node(pair["anchor"])
        G.add_node(pair["positive"])
        G.add_edge(pair["anchor"], pair["positive"])
        G.add_edge(pair["positive"], pair["anchor"])
        
    
    # Objective is to mine the negative that are not member of the components of anchor and positive
    for pair in tqdm(champion_pairs):
        anchor : str = pair["anchor"]
        positive : str = pair["positive"]
        
        # Getting the connected component of anchor and positive
        connected_components = nx.node_connected_component(G, anchor)
        
        # collect one representative negative from each other connected component
        negatives = []
        for comp in nx.connected_components(G):
            if comp == connected_components:
                continue
            
            # pick a random representative that's not anchor or positive
            flag = True
            l_comp = list(comp)
            random.shuffle(l_comp)
            i = 0
            while flag and i < len(l_comp):
                candidate = l_comp[i]
                if candidate != anchor and candidate != positive:
                    negatives.append(candidate)
                    flag = False
                i += 1
        
        for negative in negatives:
            if not(os.path.exists("./data/contrastive/champion_triplets.jsonl")):
                open_mode : str = "w"
            else:
                open_mode : str = "a"
            
            with open("./data/contrastive/champion_triplets.jsonl", open_mode) as o:
                o.write(json.dumps({"anchor": anchor, "positive": positive, "negative": negative}) + "\n")
    
    
    