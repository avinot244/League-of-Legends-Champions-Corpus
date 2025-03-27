from pydantic import BaseModel
from dataclasses import dataclass, field


class MonsterModel(BaseModel):
    monster_rewards: str
    general_description: str
    gameplay: str

@dataclass
class MonsterModelWrapper:
    model : dict = field(default_factory=lambda: MonsterModel.model_json_schema())
    prompt : str = "Extract all content from the Monster Rewards section, the Gameplay section and include the general description. Replace all the links by their corresponding replacement text\n\nFormat the content in markdown"

