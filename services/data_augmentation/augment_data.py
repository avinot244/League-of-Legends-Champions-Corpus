import json
import uuid
from tqdm import tqdm

from services.data_augmentation.champion_role_profile import champion_role_profile, get_list_id
from services.data_augmentation.paraphrasing import paraphrase_text
from services.data_augmentation.prompt_response import prompt_response
from packages.globals import CHUNK_SIZE, CHUNK_OVERLAP, N_CHUNKS
from transformers import AutoTokenizer


def augment_data_with_prompt(output_path : str):
    augmented_data : list[dict] = []
    id_list_champs : list[str] = get_list_id()
    print(f"{output_path}augmented_data.jsonl")
    with open(f"{output_path}lol-champs.jsonl", "r") as f:
        lines = f.readlines()
        for line in tqdm(lines[:10]):
            data : dict = json.loads(line)
            id : str = data["id"]
            
            if id in id_list_champs:
                new_data : dict = dict()
                new_data["id"] = str(uuid.uuid4())
                new_data["label"] = data["label"]
                new_data["text"] = champion_role_profile(data["label"], data["text"])
                augmented_data.append(new_data)
                
            new_data : dict = dict()
            new_data["id"] = str(uuid.uuid4())
            new_data["label"] = data["label"]
            new_data["text"] = paraphrase_text(data["text"])
            augmented_data.append(new_data)
            
            with open(f"{output_path}augmented_data.jsonl", "w") as o:
                for d in augmented_data:
                    o.write(json.dumps(d) + "\n")


def count_tokens(text: str) -> int:
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)                  

def prompt_response_augmentation(output_path : str):
    augmented_data : list[dict] = []
    with open(f"{output_path}lol-champs.jsonl", "r") as f:
        lines = f.readlines()
        chunk : str = ""
        for line in tqdm(lines[:10]):
            data : dict = json.loads(line)
            current_size : int = count_tokens(chunk)
            if current_size + count_tokens(data["text"]) <= CHUNK_SIZE:
                chunk += " " + data["text"]
            
            else:
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
                    with open(f"{output_path}augmented_data.jsonl", "w") as o:
                        for d in augmented_data:
                            o.write(json.dumps(d) + "\n")
            


def augment_data(output_path : str):
    # augment_data_with_prompt(output_path)
    prompt_response_augmentation(output_path)
    
    
    