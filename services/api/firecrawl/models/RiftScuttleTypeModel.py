from pydantic import BaseModel
from dataclasses import dataclass, field

class Gameplay(BaseModel):
    description: str
    gameplay_interactions: str

class RiftScuttleTypeModel(BaseModel):
    page_title: str
    general_description: str
    ability_description: str
    spawn: str
    gameplay: Gameplay
    
    
@dataclass
class RiftScuttleTypeModelWrapper:
    model: dict = field(default_factory=lambda: RiftScuttleTypeModel.model_json_schema())
    prompt: str = "Extract the page title, all the general description content, all the detailed description content, all the spawn content and all the gameplay content. Replace any lnks by their corresponding replacement texts"