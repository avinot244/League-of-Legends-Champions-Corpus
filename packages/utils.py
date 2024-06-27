
import json
import re
from transformers import pipeline

def saveToJson(data_dict : dict, json_path : str):
    with open(json_path, 'r') as file:
        data = json.load(file)

    data['row'].append(data_dict)

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)



def get_SnW_body(championName : str):
    res : str = "{\"operationName\": \"LolChampionGuidesTabStaticQuery\",\"variables\": {\"championFilter\": \"data/slug/iv eq '{}'\",\"allRolesDataFilter\": \"data/championSlug/iv eq '{}'\",\"junglePathFilter\": \"data/championSlug/iv eq '{}'\"},\"query\": \"query LolChampionGuidesTabStaticQuery($championFilter: String!, $junglePathFilter: String!, $allRolesDataFilter: String!) {\n  guidesByRoleData: queryChampionsRoleDataV2Contents(filter: $allRolesDataFilter) {\n    flatData {\n      ...LolChampionGuideFragment\n      __typename\n    }\n    __typename\n  }\n  guidesJunglePath: queryChampionJunglePathV1Contents(filter: $junglePathFilter) {\n    flatData {\n      ...LolChampionGuideJunglePathingFragment\n      __typename\n    }\n    __typename\n  }\n  seoOverride: queryChampionsSeoV1Contents(filter: $championFilter) {\n    flatData {\n      slug\n      championGuidesMetaTitle\n      championGuidesMetaDesc\n      championGuidesOgImage\n      championGuidesPageHeaderSeoText\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LolChampionGuideFragment on ChampionsRoleDataV2DataFlatDto {\n  championSlug\n  role\n  strengths\n  weaknesses\n  howToPlayVideo\n  __typename\n}\n\nfragment LolChampionGuideJunglePathingFragment on ChampionJunglePathV1DataFlatDto {\n  championSlug\n  imageUrl\n  side\n  title\n  __typename\n}\n\"}".format(championName, championName, championName)
    
    return res

def get_powerSpikes_body(championName : str) :
    res : str = "{\"operationName\": \"LolChampionPageStaticQuery\",\"variables\": {\"championFilter\": \"data/slug/iv eq '" +championName + "'\".format(championName),\"allRolesDataFilter\": \"data/championSlug/iv eq '" +championName + "'\".format(championName),\"expertGuideFilter\": \"data/championSlug/iv eq '" +championName + "'\".format(championName)},\"query\": \"query LolChampionPageStaticQuery($championFilter: String!, $allRolesDataFilter: String!, $expertGuideFilter: String!) {\n  championCommonInfo: queryChampionsV1Contents(filter: $championFilter) {\n    flatData {\n      riotId\n      damage\n      slug\n      name\n      title\n      lore\n      tags\n      type {\n        flatData {\n          slug\n          name\n          __typename\n        }\n        __typename\n      }\n      difficulty {\n        flatData {\n          slug\n          name\n          color\n          level\n          __typename\n        }\n        __typename\n      }\n      customDifficulty {\n        flatData {\n          slug\n          name\n          color\n          level\n          __typename\n        }\n        __typename\n      }\n      abilities {\n        flatData {\n          slug\n          name\n          activationKey\n          __typename\n        }\n        __typename\n      }\n      difficultyLevel\n      moderators {\n        flatData {\n          ...ModeratorFragment\n          __typename\n        }\n        __typename\n      }\n      damageType\n      playStyle\n      socialCommunities {\n        slug\n        url\n        __typename\n      }\n      preMobility\n      preToughness\n      preControl\n      preDamage\n      __typename\n    }\n    __typename\n  }\n  powerSpikesData: queryChampionsRoleDataV2Contents(filter: $allRolesDataFilter) {\n    flatData {\n      role\n      championSlug\n      gameStages {\n        gamePlan\n        gameStage\n        powerSpike\n        powerSpikeDescription\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  championAds: queryChampionsAdsV1Contents(filter: $championFilter) {\n    flatData {\n      ...LolChampionAdsFragment\n      __typename\n    }\n    __typename\n  }\n  buildGuide: queryLolChampionsExpertGuidesContents(filter: $expertGuideFilter) {\n    flatData {\n      ...ChampionExpertGuideFragment\n      __typename\n    }\n    __typename\n  }\n  seoOverride: queryChampionsSeoV1Contents(filter: $championFilter) {\n    flatData {\n      expertGuidePageTitle\n      expertGuidePageDesc\n      expertGuideOgImage\n      championExpertGuidesPageHeaderSeoText\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ModeratorFragment on ModeratorsV1DataFlatDto {\n  summonerName\n  region\n  rank\n  division\n  icon\n  links {\n    slug\n    link\n    __typename\n  }\n  shortBio\n  __typename\n}\n\nfragment LolChampionAdsFragment on ChampionsAdsV1DataFlatDto {\n  hBanner {\n    flatData {\n      alt\n      basePath\n      items {\n        maxWidth\n        prefix\n        x2Prefix\n        __typename\n      }\n      imgTrackingCode\n      linkUrl\n      slug\n      type\n      types\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChampionExpertGuideFragment on LolChampionsExpertGuidesDataFlatDto {\n  championSlug\n  championRoles\n  difficulty {\n    flatData {\n      slug\n      name\n      index\n      color\n      __typename\n    }\n    __typename\n  }\n  videoUrl\n  placeholderImage\n  expertVideoGuideTimestamps {\n    name\n    time\n    __typename\n  }\n  __typename\n}\n\"}"
    return res

def replace_within_double_curly_brackets(text):
    if text == None:
        return ""
    # Regular expression to find substrings within double curly braces
    pattern = r'{{(.*?)}}'

    # Find all matches
    matches = re.findall(pattern, text)

    # Replace each match with its last character
    for match in matches:
        last_char = match[-1] if match else ''
        text = text.replace('{{' + match + '}}', last_char)

    return text


def get_token(option : str):
    
    with open("./token.json", "r") as f:
        res = json.load(f)
        if option == "read":
            return res["read"]
        elif option == "write":
            return res["write"]
        



def augment_data(text : str):
    pipe_en_fr = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
    pipe_fr_en = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

    text_fr = pipe_en_fr(text)[0]['translation_text']
    text_en = pipe_fr_en(text_fr)[0]['translation_text']
    return text_en
