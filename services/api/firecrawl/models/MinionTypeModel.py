from pydantic import BaseModel
from dataclasses import dataclass

class MinionWaves(BaseModel):
    description: str
    details: list[str]

class SideLaneSpeed(BaseModel):
    description: str
    details: list[str]

class MinionPushing(BaseModel):
    sumonners_rift: str
    howling_abyss: str

class Buffs(BaseModel):
    general: str
    sidelane_speed: SideLaneSpeed
    minion_pushing: MinionPushing

class MinionTypeModel(BaseModel):
    page_title: str
    general_descrition: str
    spawning_location_and_routes: str
    minion_waves: MinionWaves
    behavior: str
    priority: str
    timing: str
    vision: str
    stats_mechanics: list[str]
    buffs: Buffs
    creep_score: str
    wave_gold_value: str
    wave_strategy: list[str]
    game_terminology: list[str]
    
@dataclass
class MinionTypeModelWrapper:
    model: dict = MinionTypeModel.model_json_schema()
    prompt: str =  "Extract all the page textual content except for the navigation menus. Replace any links by their corresponding replacement text"
    