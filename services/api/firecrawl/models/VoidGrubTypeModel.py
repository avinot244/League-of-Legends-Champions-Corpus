from pydantic import BaseModel
from dataclasses import dataclass

class VoidGrubTypeModel(BaseModel):
    general_description: str
    notes: list[str]
    spawn_group: str
    passives: list[str]

@dataclass
class VoidGrubTypeModelWrapper:
    model: dict = VoidGrubTypeModel.model_json_schema()
    prompt: str = "Extract the general description, all spawn groub content, all passives content, and all notes content. Replace any links with their corresponding replacement texts."