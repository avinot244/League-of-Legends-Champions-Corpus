import json
from services.api.firecrawl.api_calls_firecrawl import scrape, extract
from tqdm import tqdm
import time
import ollama
import os

from packages.globals import DATASETS_PATH
from packages.types import t_data_type
from services.prompt_provider.prompt_provider import get_prompt



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
    for data_type in data_type_list:
        if not os.path.exists(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json"):
            extract_data(data_type, error_mode)
        
    for data_type in data_type_list:
        if os.path.exists(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json"):
            out_data_list : list[dict] = list()
            prompt : str = get_prompt(data_type)
            with open(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json", "r") as f:
                print(f"Serializing {data_type} data")
                data : list[dict] = json.load(f)
                for json_data in tqdm(data):
                    try:
                        str_data : str = ollama.chat(
                            model="json_serializer:latest",
                            messages=[
                                {
                                    "role": "system",
                                    "content": prompt
                                },
                                {
                                    "role": "user",
                                    "content": f"<json>\n{json.dumps(json_data, indent=4)}\n</json>"
                                }
                            ]
                        ).message["content"].replace("$", "")
                        out_data_list.append({
                            "label": json_data["name"],
                            "text": str_data
                        })
                        with open(f"{DATASETS_PATH}/wiki/wiki_data_str_{data_type}.json", "w") as o:
                            json.dump(out_data_list, o, indent=4)
                    
                    except Exception as e:
                        print(e)
                        print(f"Error serializing {data_type} data: {e}")
                        continue