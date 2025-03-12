from pydantic import BaseModel
from typing import get_args, Union

from services.api.firecrawl.models import *
from services.api.firecrawl.types import *

def model_provider(url : str) -> Union[ChampionModelWrapper, MainRuneModelWrapper, MainTreeRuneModel, SubRuneModelWrapper, MonsterModelWrapper]:
    data_value : str = url.split("/")[-1]
    
    if data_value in get_args(champions):
        return ChampionModelWrapper
    if data_value in get_args(main_tree_rune):
        return MainTreeRuneModel
    if data_value in get_args(main_rune):
        return MainRuneModelWrapper
    if data_value in get_args(sub_rune):
        return SubRuneModelWrapper
    else:
        return Exception(f"Element {data_value} not supported")
