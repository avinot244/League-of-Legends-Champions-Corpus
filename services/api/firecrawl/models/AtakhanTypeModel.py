from pydantic import BaseModel
from dataclasses import dataclass, field

class AtakhanTypeModel(BaseModel):
    name: str
    overall_description: str
    detailed_abilities: str
    passives: str
    attacks_and_abilities: str
    rewards: str
    
@dataclass
class AtakhanTypeModelWrapper:
    model: dict = field(default_factory=lambda: AtakhanTypeModel.model_json_schema())
    prompt: str = "Extract the name of the monster, its overall description, detailed abilities, spawn mechanic, passives, all attacks and abilities, and all rewards. Replace any links with their corresponding replacement text."
    