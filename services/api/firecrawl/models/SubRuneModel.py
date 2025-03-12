from pydantic import BaseModel
from dataclasses import dataclass

class SubRuneModel(BaseModel):
    name: str
    description: str
    strategy: str
    notes: list[str]

@dataclass
class SubRuneModelWrapper:
    model: dict = SubRuneModel.model_json_schema()
    prompt: str = "Extract the name, description, notes, and strategy sections. Replace all links with their replacement texts. Format the extracted text in markdown."