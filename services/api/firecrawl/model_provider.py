from typing import get_args

from services.api.firecrawl.models import *
from services.api.firecrawl.types import *

def model_provider(url : str) -> ModelClass:
    data_value : str = url.split("/")[-1]
    
    if data_value in get_args(champions):
        return ChampionModelWrapper()
    if data_value in get_args(main_tree_rune):
        return MainTreeRuneModel()
    if data_value in get_args(main_rune):
        return MainRuneModelWrapper()
    if data_value in get_args(sub_rune):
        return SubRuneModelWrapper()
    if data_value in get_args(dragon_types):
        return DragonTypeModelWrapper()
    if data_value in get_args(jungle_camps_types):
        return JungleCampModelWrapper()
    if data_value == "Baron_Nashor":
        return NashorTypeModelWrapper()
    if data_value == "Atakhan":
        return AtakhanTypeModelWrapper()
    if data_value == "Monster":
        return MonsterModelWrapper()
    if data_value == "Voidgrub_camp":
        return VoidGrubTypeModelWrapper()
    if data_value == "Rift_Scuttler_camp":
        return RiftScuttleTypeModelWrapper()
    if data_value == "Minion":
        return MinionTypeModelWrapper()
    if data_value == "Rift_Herald":
        return RiftHeraldTypeModelWrapper()
    if data_value in get_args(summoner_type):
        return SummonerSpellModelWrapper()
    if data_value in get_args(item_types):
        return ItemModelWrapper()
    if data_value == "Champion_classes":
        return MainClassModelWrapper()
    if data_value in get_args(classes):
        return ChampionClassModelWrapper()
    if data_value == "Lanes":
        return LanesModelWrapper()
    
    else:
        return Exception(f"Element {data_value} not supported")
