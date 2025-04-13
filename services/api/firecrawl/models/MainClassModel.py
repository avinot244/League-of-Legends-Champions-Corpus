from pydantic import BaseModel
from dataclasses import dataclass

class DescriptionElement(BaseModel):
    title: str
    content: str


class MainClassModel(BaseModel):
    title: str
    general_description: str
    detailed_description: list[DescriptionElement]
    detailed_interaction: list[DescriptionElement]
    other_attributes: list[DescriptionElement]
    
@dataclass
class MainClassModelWrapper:
    model: dict = MainClassModel.model_json_schema()
    prompt: str = "Extract the title of the page, the general description, all detailed definitions, all the detailed interactions, and other attributes with their titles and content. Don't do any summarisation extract all the content. Replace any links by their corresponding replacement text."