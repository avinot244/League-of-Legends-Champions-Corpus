from pydantic import BaseModel
from dataclasses import dataclass

class MainSummonerSpellModel(BaseModel):
    general_description: str
    standard_summoner_spells: list[str]
    variants: list[str]
    cooldown_reducing_effects: list[str]
    
@dataclass
class MainSummonerSpellModelWrapper:
    model: dict = MainSummonerSpellModel.model_json_schema()
    prompt: str = "Extract the general description, list of standard summoner spells, all variants, and cooldown reducing effects. Replace any kinks by their replacement text."
    