from pydantic import BaseModel
from typing import get_args

from services.api.firecrawl.models import *
from services.api.firecrawl.types import *

def model_provider(url : str) -> BaseModel:
    data_value : str = url.split("/")[-1]
    
    if data_value in get_args(champions):
        return ChampionModel
    if data_value in get_args(main_tree_rune):
        return MainTreeRuneModel
    if data_value in get_args(main_rune):
        return MainRuneModel
    if data_value in get_args(sub_rune):
        return SubRuneModel
    else:
        return Exception(f"Element {data_value} not supported")
