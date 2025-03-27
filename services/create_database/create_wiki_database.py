from typing import Literal
import json
from services.api.firecrawl.api_calls_firecrawl import scrape, extract
from tqdm import tqdm
import time

from packages.globals import DATASETS_PATH

def extract_data(data_type : Literal["champions", "game_mechanics", "items", "runes", "summonner_spells"], error_mode : bool = False):
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
    
    for url in tqdm(url_list):
        try :
            result = extract(url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki/wiki_data_{data_type}.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)

def create_wiki_database(error_mode : bool = False):    
    for data_type in ["champions", "game_mechanics", "items", "runes", "summonner_spells"]:
        extract_data(data_type, error_mode)