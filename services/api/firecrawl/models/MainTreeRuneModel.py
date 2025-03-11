from pydantic import BaseModel

class MainTreeRuneModel(BaseModel):
    rune_description: str
    overall_purpose: str