from pydantic import BaseModel
from dataclasses import dataclass, field

class JungleCampModel(BaseModel):
    page_title: str
    general_description: str
    notes: list[str]
    strategy: list[str]
    
@dataclass
class JungleCampModelWrapper:
    model: dict = field(default_factory=lambda: JungleCampModel.model_json_schema())
    prompt: str = "Extract the page title, all the general description content, all the notes, and all the content of the strategy section if it exists. Replace any links by their corresponding replacement texts"