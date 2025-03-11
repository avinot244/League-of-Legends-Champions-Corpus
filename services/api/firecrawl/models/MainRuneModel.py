from pydantic import BaseModel    

class Rune(BaseModel):
    name: str
    all_effects_description: str
    all_notes: list[str]

class MainRuneModel(BaseModel):
    runes: list[Rune]