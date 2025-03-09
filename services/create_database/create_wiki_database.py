from typing import Literal
import json
from services.api.firecrawl.api_calls_firecrawl import scrape, extract
from tqdm import tqdm

from packages.globals import DATASETS_PATH, LOL_WIKI_URL


def create_wiki_database(mode : Literal["scrape", "extract"], error_mode : bool = False):    
    champion_list : list[str] = list()
    error_list : list[str] = list()
    if not(error_mode):
        with open(f"{DATASETS_PATH}/champion_mapping.json", "r") as f:
            champion_list = json.load(f)
    else:
        with open(f"./error_fircrawl.json", "r") as f:
            champion_list = json.load(f)
    
    all_data : list[dict] = list()
    
    for champion in tqdm(champion_list):
        url : str = f"{LOL_WIKI_URL}{champion}"
        try :
            if mode == "scrape":
                result = scrape(url)
            elif mode == "extract":
                result = extract(url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data.json", "w") as o:
                json.dump(all_data, o, indent=4)

        except Exception as e:
            error_list.append(champion)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
    