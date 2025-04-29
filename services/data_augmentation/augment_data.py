import json
import uuid
from tqdm import tqdm
import os
import time
from typing import Literal

from services.data_augmentation.champion_role_profile import champion_role_profile, get_list_id
from services.data_augmentation.paraphrasing import paraphrase_text
from services.data_augmentation.prompt_response import prompt_response
from services.data_augmentation.champion_matchup import champion_matchup
from services.data_augmentation.champion_role import champion_role
from packages.globals import CHUNK_SIZE, CHUNK_OVERLAP, N_CHUNKS
from transformers import AutoTokenizer


def augment_data_with_prompt(output_path : str, error_path : str):
    augmented_data : list[dict] = []
    id_list_champs : list[str] = get_list_id()
    with open("./augmented_ids.json", "r") as o:
        augmented_id_list : list[str] = json.load(o)
    print("Augmenting data with prompt")
    with open(f"{output_path}lol-champs.jsonl", "r") as f:
        lines = f.readlines()
        for line in tqdm(lines[:]):
            data : dict = json.loads(line)
            id : str = data["id"]
            
            if not(data["id"] in augmented_id_list):
                time.sleep(0.9)       
                if id in id_list_champs:
                    new_data : dict = dict()
                    new_data["id"] = str(uuid.uuid4())
                    new_data["label"] = data["label"]
                    new_data["text"] = champion_role_profile(data["id"], data["label"], data["text"], error_path)
                    augmented_data.append(new_data)
                
                new_data : dict = dict()
                new_data["id"] = str(uuid.uuid4())
                new_data["label"] = data["label"]
                new_data["text"] = paraphrase_text(data["id"], data["text"], error_path)
                augmented_data.append(new_data)
                augmented_id_list.append(data["id"])
                
                if os.path.exists(f"{output_path}augmented_data.jsonl"):
                    open_mode = "a"
                else:
                    open_mode = "w"
                
                with open(f"{output_path}augmented_data.jsonl", open_mode) as o:
                    for d in augmented_data:
                        o.write(json.dumps(d) + "\n")
                        
                with open(f"./augmented_ids.json", "w") as o:
                    json.dump(augmented_id_list, o, indent=4)
                    
                augmented_data : list[dict] = []


def count_tokens(text: str) -> int:
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)                  

def prompt_response_augmentation(output_path : str):
    augmented_data : list[dict] = []
    print("Augmenting data with prompt response")
    with open(f"{output_path}lol-champs.jsonl", "r") as f:
        lines = f.readlines()
        chunk : str = ""
                
        for line in tqdm(lines[2669:]):
            data : dict = json.loads(line)
            current_size : int = count_tokens(chunk)
            if current_size + count_tokens(json.dumps(data)) <= CHUNK_SIZE:
                chunk += "\n" + json.dumps(data)
            
            else:
                time.sleep(0.9)
                qa_pairs : list[dict] = prompt_response(chunk, n=5)
                if len(qa_pairs) == 0:
                    print("No qa pairs generated")
                else:
                    for qa in qa_pairs:
                        new_data : dict = dict()
                        new_data["id"] = str(uuid.uuid4())
                        new_data["label"] = data["label"]
                        new_data["text"] = qa
                        augmented_data.append(new_data)

                    chunk = data["text"]
                    
                    if os.path.exists(f"{output_path}augmented_data.jsonl"):
                        open_mode = "a"
                    else:
                        open_mode = "w"
                        
                    with open(f"{output_path}augmented_data.jsonl", open_mode) as o:
                        for d in augmented_data:
                            o.write(json.dumps(d) + "\n")
                                
                                
def get_champion_card(champion : str, output_path : str):
    with open(f"{output_path}augmented_data-prompt.jsonl", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            if champion.lower() in data["label"].lower() and data["text"][0] == "#":
                return data["text"]

def champion_matchup_augmentation(output_path : str, error_path : str):
    chunk : list = list()
    chunk_against : list = list()
    
    champion_list : list[str] = list()
    with open("./data/champion_mapping.json", "r") as c:
        data : list[dict] = json.load(c)
        champion_list = [d["name"] for d in data] 
    
    with open(f"{output_path}mobalytics.jsonl", "r") as f:
        lines = f.readlines()
        for champion in tqdm(champion_list):
            time.sleep(10)
            for line in lines:
                data = json.loads(line)
                if champion.lower() in data["label"].lower():
                    if 'against' in data["label"].lower():
                        chunk_against.append(data["text"])
                    else:
                        if data["text"] not in chunk:
                            chunk.append(data["text"])
            
            champion_card = get_champion_card(champion, output_path)
            if champion_card != None:
                            
                augmented_data_list : list[dict] = champion_matchup(
                    champion,
                    " ".join(chunk),
                    champion_card,
                    " ".join(chunk_against),
                    error_path
                )
                
                augmented_data : list[dict] = [{"id": str(uuid.uuid4()), "label": f"Against {champion}", "text": d["description"]} for d in augmented_data_list]
                
                if os.path.exists(f"{output_path}augmented_data_mu.jsonl"):
                    open_mode = "a"
                else:
                    open_mode = "w"
                
                with open(f"{output_path}augmented_data_mu.jsonl", open_mode) as o:
                    for d in augmented_data:
                        o.write(json.dumps(d) + "\n")

def champion_role_augmentation(output_path : str, error_path : str):
    champion_list : list[str] = list()
    with open("./data/champion_mapping.json", "r") as c:
        data : list[dict] = json.load(c)
        champion_list = [d["name"] for d in data]
        
    with open(f"{output_path}mobalytics.jsonl", "r") as f:
        lines = f.readlines()
        for champion in tqdm(champion_list):
            time.sleep(10)
            for line in lines:
                champion_card = get_champion_card(champion, output_path)
                if champion_card != None:
                    augmented_data : str = champion_role(champion_card, error_path)
                    
                    if os.path.exists(f"{output_path}augmented_data_role.jsonl"):
                        open_mode = "a"
                    else:
                        open_mode = "w"
                    
                    with open(f"{output_path}augmented_data_role.jsonl", open_mode) as o:
                        o.write(json.dumps({"id": str(uuid.uuid4()), "label": champion, "text": augmented_data}) + "\n")
        

def augment_data(output_path : str, error_path : str, mode : Literal["para/profile", "QA", "mu", "role"]):
    if mode == "para/profile":
        augment_data_with_prompt(output_path, error_path)
    elif mode == "QA":
        prompt_response_augmentation(output_path, error_path)
    elif mode == "mu":
        champion_matchup_augmentation(output_path, error_path)
    elif mode == "role":
        champion_role_augmentation(output_path, error_path)
    
    
    