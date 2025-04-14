from pydantic import BaseModel
from dataclasses import dataclass, field


class PositionModel(BaseModel):
    position_name: str
    description: str
    
    
class LanesModel(BaseModel):
    name: str
    general_description: str
    summoners_rift_description: str
    positions: list[PositionModel]
    

@dataclass
class LanesModelWrapper:
    model: dict = field(default_factory=lambda: LanesModel.model_json_schema())
    prompt: str = "Extract the page name, the general description, the general description for Summoner's Rift and the detailed description for each positions. Do not summarize the content and replace any links with their corresponding replacement text."