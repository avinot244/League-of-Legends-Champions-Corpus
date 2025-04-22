import json
import uuid
from tqdm import tqdm
import os
import time

from services.data_augmentation.champion_role_profile import champion_role_profile, get_list_id
from services.data_augmentation.paraphrasing import paraphrase_text
from services.data_augmentation.prompt_response import prompt_response
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
                
        for line in tqdm(lines[:]):
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
                                
            


def augment_data(output_path : str, error_path : str):
    # augment_data_with_prompt(output_path, error_path)
    prompt_response_augmentation(output_path)
    
    
    