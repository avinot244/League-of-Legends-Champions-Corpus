from pydantic import BaseModel
from dataclasses import dataclass, field

class Passives(BaseModel):
    description: str
    passive_list: list[str]

class BasicAttacks(BaseModel):
    description: str
    basic_attack_list: list[str]
    
class Abilities(BaseModel):
    description: str
    ability_list: list[str]

class NashorTypeModel(BaseModel):
    page_title: str
    general_description: str
    spawn: list[str]
    passives: Passives
    basic_attacks: BasicAttacks
    abilities: Abilities
    strategy: str

@dataclass
class NashorTypeModelWrapper:
    model: dict = field(default_factory=lambda: NashorTypeModel.model_json_schema())
    prompt: str = "Extract the general description, all spawn content, all passives content, all basic attacks content, all abilities content and all strategies. Replace any links with their corresponding replacement texts."