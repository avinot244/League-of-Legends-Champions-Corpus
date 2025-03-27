from pydantic import BaseModel
from dataclasses import dataclass, field

class MainTreeRuneModel(BaseModel):
    description_content: str
    notes: list[str]

@dataclass
class MainTreeRuneModelWrapper:
    model: dict = field(default_factory=lambda: MainTreeRuneModel.model_json_schema())
    prompt: str = "Extract all the description content and subsections. Also extract all the notes. Replace the links by their replacement texts. Format the extracted text in markdown."