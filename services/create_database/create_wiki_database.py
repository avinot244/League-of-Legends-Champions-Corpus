from typing import Literal
import json
from services.api.firecrawl.api_calls_firecrawl import scrape, extract
from tqdm import tqdm
import time

from packages.globals import DATASETS_PATH, LOL_WIKI_URL


def create_wiki_database(error_mode : bool = False):    
    champion_list : list[str] = list()
    error_list : list[str] = list()
    
    if not(error_mode):
        with open(f"{DATASETS_PATH}/champion_mapping.json", "r") as f:
            champion_list = json.load(f)
    else:
        with open(f"./error_firecrawl.json", "r") as f:
            champion_list = json.load(f)
            
    with open(f"{DATASETS_PATH}/lol-wiki-urls/game_mechanics.json", "r") as f:
        game_mechanics_urls : list[str] = json.load(f)
        
    with open(f"{DATASETS_PATH}/lol-wiki-urls/items.json", "r") as f:
        items_urls : list[str] = json.load(f)
        
    with open(f"{DATASETS_PATH}/lol-wiki-urls/runes.json", "r") as f:
        runes_urls : list[str] = json.load(f)
        
    with open(f"{DATASETS_PATH}/lol-wiki-urls/summonner_spells.json", "r") as f:
        summonner_spells_urls : list[str] = json.load(f)
    
    all_data : list[dict] = list()
    
    print("Scraping champions")
    for champion in tqdm(champion_list):
        url : str = f"{LOL_WIKI_URL}{champion}"
        try :
            result = extract(url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data_champions.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(champion)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
    
    print("Scraping game mechanics")
    for game_mechanic_url in tqdm(game_mechanics_urls):
        try :
            result = extract(game_mechanic_url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data_game_mechanics.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(game_mechanic_url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
    
    print("Scraping items")
    for item_url in tqdm(items_urls):
        try :
            result = extract(item_url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data_items.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(item_url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
    
    print("Scraping runes")
    for rune_url in tqdm(runes_urls):
        try :
            result = extract(rune_url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data_runes.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(rune_url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
    
    print("Scraping summonner spells")
    for summonner_spell_url in tqdm(summonner_spells_urls):
        try :
            result = extract(summonner_spell_url)
            all_data.append(result)
            with open(f"{DATASETS_PATH}/wiki_data_summonner_spells.json", "w") as o:
                json.dump(all_data, o, indent=4)
            time.sleep(6)
        except Exception as e:
            tqdm.write(e)
            error_list.append(summonner_spell_url)
            with open("./error_firecrawl.json", "w") as o:
                json.dump(error_list, o, indent=4)
        
    