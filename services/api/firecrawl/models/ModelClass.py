from dataclasses import dataclass, field

from abc import ABC

@dataclass
class ModelClass(ABC):
    model: dict = field(default_factory=dict)
    prompt: str