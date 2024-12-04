from transformers import AutoTokenizer
from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5_fast import T5TokenizerFast
from transformers.pipelines.text2text_generation import TranslationPipeline
from transformers import logging
import json
import ollama

from .utils.globals import PROMPT_PROPOSITIONIZER, PROMPT_PROPOSITIONIZER_V2

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

def propositionizer(
    title : str, 
    section : str, 
    content : str, 
    model : T5ForConditionalGeneration,
    tokenizer : T5TokenizerFast,
    device : str
) -> list[str]:
    splitted_content : list[str] = split_text(content, tokenizer)
    
    res : list[str] = []
    
    for content_split in splitted_content:
        input_text = f"Title: {title}. Section: {section}. Content: {content_split}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        outputs = model.generate(input_ids.to(device), max_new_tokens=512).cpu()
        
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        try:
            prop_list = json.loads(output_text)
            res += prop_list
        except:
            prop_list = []
            print("[ERROR] Failed to parse output text as JSON.")
        
        
    return res

def propositioner_llama(
    title : str,
    section : str,
    content : str
) -> str: 
    logging.set_verbosity_error()

    # Propositionizing the content
    input_text = f"Decompose the following:\nTitle: {title}. Section: {section}. Content: {content}"

    chat_history : list[dict] = list()
    chat_history.append({
        "role": "system",
        "content": PROMPT_PROPOSITIONIZER_V2
    })

    chat_history.append({
        "role": "user",
        "content": input_text
    })

    response = ollama.chat("llama3.2:3b", messages=chat_history)
    
    try:
        prop_list = json.loads(response["message"]["content"])
    except:
        prop_list = []
    
    return prop_list