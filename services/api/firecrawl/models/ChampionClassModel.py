from pydantic import BaseModel
from dataclasses import dataclass, field

class SubClassModel(BaseModel):
    title: str
    strengths: str
    weaknesses: str
    detailed_description: str
    champion_list : list[str]

class ChampionClassModel(BaseModel):
    page_title: str
    general_description: str
    sublasses: list[SubClassModel]
    
@dataclass
class ChampionClassModelWrapper:
    model: dict = field(default_factory=lambda: ChampionClassModel.model_json_schema())
    prompt: str = "Extract the page title, its general description, and all of the subclasses' titles, strenghts, weaknesses, detailed descriptions and detailed champion lists without any summarization. Ensure all content is captured in full. Replace any links by their corresponding replacement text"