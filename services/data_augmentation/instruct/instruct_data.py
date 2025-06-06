import json
import uuid
from tqdm import tqdm
import os
import time
from typing import Literal

from services.data_augmentation.instruct.factual_instruct import factual_instruct
from services.data_augmentation.instruct.strategic_instruct import strategic_instruct
from services.data_augmentation.instruct.role_instruct import role_instruct

from packages.globals import CHUNK_SIZE, CHUNK_OVERLAP, N_CHUNKS
from transformers import AutoTokenizer


def count_tokens(text: str) -> int:
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)                  


def get_champion_card(champion : str, path : str):
    with open(f"{path}augmented_data-prompt.jsonl", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            if champion.lower() == data["label"].lower() and data["text"][0] == "#":
                return data["text"], data["id"]
            
    return None, None
# One function for instruct factual, strategic and role

def instruct_factual_generation(input_path : str, output_path : str, error_path : str, fix_error : bool) -> None:
    with open(f"{input_path}lol-corpus.jsonl", "r") as f:
        lines = f.readlines()
        
        chunk : str = ""
        id : str = json.loads(lines[4295])["id"]
        for line in tqdm(lines[4296:]):
            data = json.loads(line)
            
            if count_tokens(chunk) + count_tokens(data["text"]) < CHUNK_SIZE:
                chunk += " " + data["text"]
                
            else:
                time.sleep(1)
                id = data["id"]
                chunk = data["text"]
                qa_list : list[dict] = factual_instruct(chunk, 5, error_path, id)
                
                if qa_list != None:
                    if os.path.exists(f"{output_path}factual-instruct.jsonl"):
                        open_mode = "a"
                    else:
                        open_mode = "w"
                    
                    with open(f"{output_path}factual-instruct.jsonl", open_mode) as o:
                        for d in qa_list:
                            o.write(json.dumps({"id": str(uuid.uuid4()), "label": "instruct-factual", "question": d["question"], "answer": d["answer"]}) + "\n")

def instruct_strategic_generation(input_path : str, output_path : str, error_path : str, fix_error : bool) -> None:
    file_name_list : list[str] = ["mobalytics-v2.jsonl", "augmented_data_mu.jsonl", "wiki_data_chunks_game_mechanics.jsonl", "wiki_data_chunks_items.jsonl", "wiki_data_chunks_runes.jsonl"]
    
    for file_name in file_name_list[2:]:
        with open(f"{input_path}{file_name}", "r") as i:
            lines = i.readlines()
            
            chunk : list[dict] = [json.loads(lines[0])]
            for line in tqdm(lines[:]):
                label_list : list[str] = [d["label"] for d in chunk]
                data : dict = json.loads(line)
                current_size : int = sum([count_tokens(d["text"]) for d in chunk])
                if data["label"] in label_list and current_size + count_tokens(data["text"]) < CHUNK_SIZE:
                    chunk.append(data)
                else:
                    time.sleep(1)
                    context : str = " ".join([d["text"] for d in chunk])
                    id : str = chunk[0]["id"]
                    label : str = f"instruct-strategic-{chunk[0]["label"].replace(" ", "-")}"
                    chunk : list[dict] = [data]
                    qa_list : list[dict] = strategic_instruct(context, 5, error_path, id)
                    if qa_list != None:
                    
                        if os.path.exists(f"{output_path}strategic-instruct.jsonl"):
                            open_mode = "a"
                        else:
                            open_mode = "w"
                        
                        with open(f"{output_path}strategic-instruct.jsonl", open_mode) as o:
                            for qa_pair in qa_list:
                                o.write(json.dumps({"id": str(uuid.uuid4()), "label": label, "question": qa_pair["question"], "answer": qa_pair["answer"]}) + "\n")
                            
def instruct_role_generation(input_path : str, output_path : str, error_path : str, fix_error : bool) -> None:
    if fix_error:
        with open(f"{error_path}", "r") as e:
            error_data = json.load(e)
            error_id_list : list[str] = error_data["ids"]
    
    
    with open(f"{input_path}augmented_data_role.jsonl", "r") as i:
        lines = i.readlines()
        
        start = 1
        chunk : list[dict] = [json.loads(lines[start-1])]
        for line in tqdm(lines[start:]):
            data : dict = json.loads(line)
            label : str = f"instruct-role-{chunk[0]["label"].replace(" ", "-")}"
            context : str = data["text"]
            time.sleep(1)
            if fix_error:
                if data["id"] in error_id_list:
                    qa_list : list[dict] = role_instruct(context, 5, error_path, data["id"])
                    if qa_list != None:
                        error_id_list.remove(data["id"])
                        with open(f"{error_path}", "w") as e:
                            error_data = {"ids": error_id_list}
                            json.dump(error_data, e, indent=4)
                        
                        if os.path.exists(f"{output_path}role-instruct.jsonl"):
                            open_mode = "a"
                        else:
                            open_mode = "w"
                        
                        with open(f"{output_path}role-instruct.jsonl", open_mode) as o:
                            for qa_pair in qa_list:
                                o.write(json.dumps({"id": str(uuid.uuid4()), "label": label, "question": qa_pair["question"], "answer": qa_pair["answer"]}) + "\n")
            else:
                qa_list : list[dict] = role_instruct(context, 5, error_path, chunk[0]["id"])
                
                if qa_list != None:
                    if os.path.exists(f"{output_path}role-instruct.jsonl"):
                        open_mode = "a"
                    else:
                        open_mode = "w"
                    
                    with open(f"{output_path}role-instruct.jsonl", open_mode) as o:
                        for qa_pair in qa_list:
                            o.write(json.dumps({"id": str(uuid.uuid4()), "label": label, "question": qa_pair["question"], "answer": qa_pair["answer"]}) + "\n")
        
    with open("./data/champion_mapping.json", "r") as c:
        data : list[dict] = json.load(c)
        champion_list = [d["name"] for d in data]
    
    for champion in tqdm(champion_list[:]):
        time.sleep(1)
        champion_card, id = get_champion_card(champion, input_path)
        if champion_card != None and id != None:
            if fix_error:
                if id in error_id_list:
                    qa_list : list[dict] = role_instruct(champion_card, 5, error_path, id)
            
                    if qa_list != None:
                        error_id_list.remove(id)
                        with open(f"{error_path}", "w") as e:
                            error_data = {"ids": error_id_list}
                            json.dump(error_data, e, indent=4)
                        if os.path.exists(f"{output_path}role-instruct.jsonl"):
                            open_mode = "a"
                        else:
                            open_mode = "w"
                        
                        with open(f"{output_path}role-instruct.jsonl", open_mode) as o:
                            for qa_pair in qa_list:
                                label : str = f"instruct-role-{champion.lower()}"
                                o.write(json.dumps({"id": str(uuid.uuid4()), "label": label, "question": qa_pair["question"], "answer": qa_pair["answer"]}) + "\n")
            else:
                
                qa_list : list[dict] = role_instruct(champion_card, 5, error_path, id)
                
                if qa_list != None:
                    if os.path.exists(f"{output_path}role-instruct.jsonl"):
                        open_mode = "a"
                    else:
                        open_mode = "w"
                    
                    with open(f"{output_path}role-instruct.jsonl", open_mode) as o:
                        for qa_pair in qa_list:
                            label : str = f"instruct-role-{champion.lower()}"
                            o.write(json.dumps({"id": str(uuid.uuid4()), "label": label, "question": qa_pair["question"], "answer": qa_pair["answer"]}) + "\n")
                
def instruct_generation(mode : Literal["factual", "strategic", "role"], input_path : str, output_path : str, error_path : str, fix_error : bool = False):
    if mode == "factual":
        instruct_factual_generation(input_path, output_path, error_path, fix_error)
    elif mode == "strategic":
        instruct_strategic_generation(input_path, output_path, error_path, fix_error)
    elif mode == "role":
        instruct_role_generation(input_path, output_path, error_path, fix_error)