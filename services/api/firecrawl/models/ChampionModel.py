from pydantic import BaseModel
from dataclasses import dataclass

class ChampionAbility(BaseModel):
    ability_name : str
    ability_description : str

class ChampionModel(BaseModel):
    name: str
    role: str
    abilities: list[ChampionAbility]

@dataclass
class ChampionModelWrapper:
    model: dict = ChampionModel.model_json_schema()
    prompt = "Extract the global description of the champion and the detailed list of his abilities. Replace all links by their replacement text. Format the text into markdown"