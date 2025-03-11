from pydantic import BaseModel    

class SubRuneModel(BaseModel):
    sub_rune_description: str
    notes: list[str]