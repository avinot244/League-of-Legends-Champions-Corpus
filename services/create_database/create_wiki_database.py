import json
from tqdm import tqdm
import time
import os
from transformers import AutoTokenizer

from packages.globals import DATASETS_PATH
from packages.utils_func import get_token
from packages.types.data_types import t_data_type
from services.prompt_provider.prompt_provider import get_prompt
from services.api.firecrawl.api_calls_firecrawl import scrape, extract
from services.chat.anthropic_chat import chat_anthropic



def extract_data(data_type : t_data_type, error_mode : bool = False):
    all_data : list[dict] = list()
    url_list : list[str] = list()
    error_list : list[str] = list()
    if error_mode:
        with open("./error_firecrawl.json", "r") as f:
            error_list = json.load(f)
        url_list = error_list
    else:
        with open(f"{DATASETS_PATH}/lol-wiki-urls/{data_type}.json", "r") as f:
            url_list = json.load(f)
    
    print(f"Extracting data for {data_type}")
    for url in tqdm(url_list):
        try :
            result = extract(url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(1)
        except Exception as e:
            error_list.append(url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)


def create_wiki_database(data_type_list : list[t_data_type], error_mode : bool = False ):
    # Extracting data
    for data_type in data_type_list:
        if not os.path.exists(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json"):
            extract_data(data_type, error_mode)
    
    # Serializing it
    for data_type in data_type_list:
        if not os.path.exists(f"{DATASETS_PATH}/wiki/wiki_data_str_{data_type}.json"):
            out_data_list : list[dict] = list()
            prompt : str = get_prompt(data_type)
            with open(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json", "r") as f:
                print(f"Serializing {data_type} data")
                data : list[dict] = json.load(f)
                for json_data in tqdm(data):
                    try:
                        prompt_ = prompt.replace("{{CHAMPION_JSON}}", json.dumps(json_data))
                        str_data : str = chat_anthropic(prompt_)
                        out_data_list.append({
                            "label": json_data["name"],
                            "text": str_data
                        })
                        with open(f"{DATASETS_PATH}/wiki/wiki_data_str_{data_type}.json", "w") as o:
                            json.dump(out_data_list, o, indent=4)
                        time.sleep(0.9)
                    except Exception as e:
                        print(e)
                        print(f"Error serializing {data_type} data: {e}")
                        continue
                    
    # Splitting it in fixed size of 512 tokens with a 100 tokens overlap
    # Load the tokenizer
    hf_read = get_token("read", "huggingface")
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_read)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Splitting the data
    for data_type in data_type_list:
        if not os.path.exists(f"{DATASETS_PATH}/wiki/wiki_data_chunks_{data_type}.jsonl"):
            with open(f"{DATASETS_PATH}/wiki/wiki_data_str_{data_type}.json", "r") as f:
                print(f"Splitting {data_type} data into chunks")
                data = json.load(f)
                output_file = f"{DATASETS_PATH}/wiki/wiki_data_chunks_{data_type}.jsonl"
                with open(output_file, "w") as o:
                    for item in tqdm(data):
                        text = item["text"]
                        label = item["label"]
                        tokens = tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]
                        token_chunks = [
                            tokens[i:i + 512]
                            for i in range(0, len(tokens), 412)  # 412 ensures 100-token overlap
                        ]
                        for chunk in token_chunks:
                            chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
                            json.dump({"label": label, "text": chunk_text}, o)
                            o.write("\n")
    