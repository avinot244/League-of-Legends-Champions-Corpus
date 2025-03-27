from pydantic import BaseModel
from dataclasses import dataclass, field

class SummonerSpellModel(BaseModel):
    name: str
    overall_description: str
    detailed_effet: str
    notes: list[str]
    strategies: list[str]

@dataclass
class SummonerSpellModelWrapper:
    model: dict = field(default_factory=lambda: SummonerSpellModel.model_json_schema())
    prompt: str = "Extract the summoner spell name, its overall description, detailed effect, all notes, and strategies. Replace the links by their corresponding replacement text."
    