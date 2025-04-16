from dataclasses import dataclass, field

from abc import ABC

@dataclass
class ModelClass(ABC):
    prompt: str
    model: dict = field(default_factory=dict)
