from transformers import AutoTokenizer
import json
import re
import os

from packages.globals import DATASETS_PATH

def labelize(text : str, label : str):
    replacements = {
        r"\bhe\b": f"{label}",
        r"\bshe\b": f"{label}",
        r"\byou\b": f"{label}",
        r"\bhis\b": f"{label}'s",
        r"\bher\b": f"{label}'s"
    }
    
    for key, value in replacements.items():
        text = re.sub(key, value, text, flags=re.IGNORECASE)
    
    return text

def chunk_text(id : str, propositions : list[str], label : str, tokenizer : AutoTokenizer):
    chunk_texts = []
    current_chunk = ""
    for proposition in propositions:
        labeled_proposition = labelize(proposition, label)
        tokenized_proposition = tokenizer.tokenize(labeled_proposition)
        if len(tokenizer.tokenize(current_chunk)) + len(tokenized_proposition) <= 512:
            current_chunk += " " + labeled_proposition
        else:
            chunk_texts.append(current_chunk.strip())
            data : dict = {
                "text": current_chunk.strip(),
                "label": label,
                "id": id
            }
            if not(os.path.exists(DATASETS_PATH + "youtube/text/all-champs.jsonl")):
                option = "w"
            else:
                option = "a+"
            with open(DATASETS_PATH + "youtube/text/all-champs.jsonl", option) as f:
                json.dump(data, f)
                f.write("\n")
            
            current_chunk = labeled_proposition
    if current_chunk != "":
        data : dict = {
            "text": current_chunk.strip(),
            "label": label,
            "id": id
        }
        if not(os.path.exists(DATASETS_PATH + "youtube/text/all-champs.jsonl")):
            option = "w"
        else:
            option = "a+"
        with open(DATASETS_PATH + "youtube/text/all-champs.jsonl", option) as f:
            json.dump(data, f)
            f.write("\n")