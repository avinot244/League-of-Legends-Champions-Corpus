# Create prompt to assign champions to its modality
# Update champion_mapping.json
import json
import os
from tqdm import tqdm

from services.data_augmentation.champion_feature.champion_features import generate_champion_features
from packages.utils_func import get_champion_description

def update_champion_feature():
    """update ./data/champion_mapping.json with prompt"""
    with open("./data/champion_mapping.json", "r") as f:
        data : list[dict] = json.load(f)
    
    
    for idx, champion_metadata in enumerate(tqdm(data)):
        champion_description : str = get_champion_description(champion_metadata["name"])
        champion_features : dict = generate_champion_features(champion_description)
        
        for k, v in champion_features.items():
            champion_metadata[k] = v
        
        data[idx] = champion_metadata
        with open("./data/champion_mapping_rich.json", "w") as o:
            json.dump(data, o, indent=4)
            
def generate_triplets(champion_metadata : str):
    ...

def generate_triplets():
    if not(os.path.exists("./data/champion_mapping_rich.json")):
        update_champion_feature()
    
    with open("./data/champion_mapping_rich.json", "w") as f:
        data : list[dict] = json.load(f)
    
    if len(data) < 170:
        update_champion_feature()
    
    generate_triplets(data)
    