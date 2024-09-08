from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import json
from tqdm import tqdm

def token_length(word : str, tokenizer):
    return len(tokenizer.tokenize(word))

def split_text(text : str, tokenizer : AutoTokenizer, max_length : int = 350):
    
    res : list[str] = []
    sentence_list : list[str] = text.split(".")
    
    chunk : str = ""
    for sentence in sentence_list:
        if token_length(chunk, tokenizer) + token_length(sentence, tokenizer) < max_length:
            chunk += f"{sentence}."
        else:
            res.append(chunk)
            chunk = ""
    res.append(chunk)
    return res

def propositionizer(title : str, section : str, content : str) -> list[str]:
    model_name = "chentong00/propositionizer-wiki-flan-t5-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    splitted_content : list[str] = split_text(content, tokenizer)
    
    res : list[str] = []
    
    for content_split in tqdm(splitted_content, leave=False, position=1):
        input_text = f"Title: {title}. Section: {section}. Content: {content_split}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        outputs = model.generate(input_ids.to(device), max_new_tokens=512).cpu()
        
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        try:
            prop_list = json.loads(output_text)
            res += prop_list
        except:
            prop_list = []
            # print("[ERROR] Failed to parse output text as JSON.")
        
        
    return res