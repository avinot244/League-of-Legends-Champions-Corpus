import requests
import json

def get_champion_mapping(json_path : str):
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json")
    dict_champions : dict = response.json()
    res : dict = dict()

    for k, v in dict_champions["data"].items():
        temp : dict = {k: v["key"]}
        res.update(temp)
    
    with open(json_path, 'w') as file:
        json.dump(res, file, indent=4)



def get_champion_SnW(championName : str) -> None:
    response = requests.post(url="https://mobalytics.gg/api/league/gql/static/v1")