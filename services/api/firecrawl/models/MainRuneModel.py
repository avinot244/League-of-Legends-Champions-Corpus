from pydantic import BaseModel    
from dataclasses import dataclass

class MainRuneModel(BaseModel):
    global_name: str
    description: list[str]
    notes: str

@dataclass
class MainRuneModelWrapper:
    model: dict = MainRuneModel.model_json_schema()
    prompt: str = "Extract the global name, the detailed descriptions and the notes. Replace the links by their replacement texts. Format the extracted text in markdown."