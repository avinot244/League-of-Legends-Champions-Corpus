from pydantic import BaseModel
from dataclasses import dataclass

class Features(BaseModel):
    general: list[str]
    passives: list[str]
    abilities: list[str]
    
class SummonedForm(BaseModel):
    general: list[str]
    passives: list[str]
    abilities: list[str]

class RiftHeraldTypeModel(BaseModel):
    overall_description: str
    features: Features
    summoned_form: SummonedForm
    notes: list[str]
    strategies: list[str]
    
@dataclass
class RiftHeraldTypeModelWrapper:
    model: dict = RiftHeraldTypeModel.model_json_schema()
    prompt: str = "Extract the overall description, all general features, passives, and abilities of the Rift Herald. Include all passives, abilities and general description of its summoned form, as well as all notes and strategies. Replace any links by its corresponding replacement text"