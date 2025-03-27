from pydantic import BaseModel
from dataclasses import dataclass, field

class ChampionAbility(BaseModel):
    ability_name : str
    ability_description : str

class ChampionModel(BaseModel):
    name: str
    role: str
    abilities: list[ChampionAbility]

@dataclass
class ChampionModelWrapper:
    model: dict = field(default_factory=lambda: ChampionModel.model_json_schema())
    prompt: str = "Extract the global description of the champion and the detailed list of his abilities. Replace all links by their replacement text. Format the text into markdown"
