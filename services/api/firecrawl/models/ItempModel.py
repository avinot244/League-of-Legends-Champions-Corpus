from pydantic import BaseModel
from dataclasses import dataclass, field

class ItemModel(BaseModel):
    recipe: list[str]
    stats: str
    passive: str
    active: str
    notes: list[str]
    strategies: list[str]
    cost_analysis: str
    name: str
    
@dataclass
class ItemModelWrapper:
    model: dict = field(default_factory=lambda: ItemModel.model_json_schema())
    prompt: str = "Extract the item's recipe, name, stats, passive, potential active, all notes, strategies, and cost analysis. Only go one depth into the recipe tree. Replace any links by its corresponding replacement text."