import json
import uuid
from tqdm import tqdm
import os
import time
from services.data_augmentation.augmentation.prompt_response import prompt_response
from packages.globals import CHUNK_SIZE, CHUNK_OVERLAP, N_CHUNKS
from transformers import AutoTokenizer


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