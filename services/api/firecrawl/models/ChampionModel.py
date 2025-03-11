from pydantic import BaseModel    

class ChampionAbility(BaseModel):
    ability_name : str
    ability_description : str

class ChampionModel(BaseModel):
    name: str
    role: str
    abilities: list[ChampionAbility]