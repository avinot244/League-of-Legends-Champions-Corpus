from typing import Literal
import json

with open('/home/avinot/League-of-Legends-Champions-Corpus/data/champion_mapping.json') as f:
    champion_mapping = json.load(f)

champions = Literal[tuple(champion_mapping)]