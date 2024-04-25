from packages.model import DataEntry
from packages.utils import saveToJson
from packages.ui.interface import displayHeader


from colorama import Fore, Back, Style

import os
import json

if __name__ == "__main__":
    temp : DataEntry = DataEntry("this is a text", "champion", "role")

    # saveToJson(temp, "./dataset.json")

    with open("./champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)

    champion_names : list[str] = list(champion_mapping.keys())

    champion_names = [s.lower() for s in champion_names]
    print(champion_names)
    


