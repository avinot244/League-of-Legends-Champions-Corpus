from pydantic import BaseModel
from dataclasses import dataclass, field

class DragonTypeModel(BaseModel):
    name: str
    description: str
    detailed_reward: str
    passives: str
    abilities: str
    notes: str
    strategies: list[str]
    tips: list[str]
    benefits: list[str]
    
@dataclass
class DragonTypeModelWrapper:
    model: dict = field(default_factory=lambda: DragonTypeModel.model_json_schema())
    prompt: str = "Replace any links by their corresponding replacement text. Extract the name of the dragon, the overall description, the detailed reward, its passives, its abilities, its notes, all of its strategies, all the tips, and all the benefits."