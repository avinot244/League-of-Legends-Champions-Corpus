from packages.utils import get_SnW_body, get_powerSpikes_body

import requests
import json

def get_champion_mapping(json_path : str):
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json")
    dict_champions : dict = response.json()
    res : dict = dict()

    for k, v in dict_champions["data"].items():
        temp : dict = {k: v["key"]}
        res.update(temp)
    
    with open(json_path, 'w') as file:
        json.dump(res, file, indent=4)



def get_champion_SnW(championName : str) -> dict:
    body = "{\"operationName\": \"LolChampionGuidesTabStaticQuery\",\"variables\": {\"championFilter\": \"data/slug/iv eq '"+ championName +"'\",\"allRolesDataFilter\": \"data/championSlug/iv eq '" + championName +"'\",\"junglePathFilter\": \"data/championSlug/iv eq '"+ championName +"'\"},\"query\": \"query LolChampionGuidesTabStaticQuery($championFilter: String!, $junglePathFilter: String!, $allRolesDataFilter: String!) {\n  guidesByRoleData: queryChampionsRoleDataV2Contents(filter: $allRolesDataFilter) {\n    flatData {\n      ...LolChampionGuideFragment\n      __typename\n    }\n    __typename\n  }\n  guidesJunglePath: queryChampionJunglePathV1Contents(filter: $junglePathFilter) {\n    flatData {\n      ...LolChampionGuideJunglePathingFragment\n      __typename\n    }\n    __typename\n  }\n  seoOverride: queryChampionsSeoV1Contents(filter: $championFilter) {\n    flatData {\n      slug\n      championGuidesMetaTitle\n      championGuidesMetaDesc\n      championGuidesOgImage\n      championGuidesPageHeaderSeoText\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LolChampionGuideFragment on ChampionsRoleDataV2DataFlatDto {\n  championSlug\n  role\n  strengths\n  weaknesses\n  howToPlayVideo\n  __typename\n}\n\nfragment LolChampionGuideJunglePathingFragment on ChampionJunglePathV1DataFlatDto {\n  championSlug\n  imageUrl\n  side\n  title\n  __typename\n}\n\"}"
    response = requests.post(url="https://mobalytics.gg/api/league/gql/static/v1",
                             data=body)
    return response.json()

def get_champion_powerSpikes(championName : str) -> dict:
    body = "{\"operationName\": \"LolChampionPageStaticQuery\",\"variables\": {\"championFilter\": \"data/slug/iv eq '" + championName + "'\",\"allRolesDataFilter\": \"data/championSlug/iv eq '" + championName + "'\",\"expertGuideFilter\": \"data/championSlug/iv eq '" + championName + "'\"},\"query\": \"query LolChampionPageStaticQuery($championFilter: String!, $allRolesDataFilter: String!, $expertGuideFilter: String!) {\n  championCommonInfo: queryChampionsV1Contents(filter: $championFilter) {\n    flatData {\n      riotId\n      damage\n      slug\n      name\n      title\n      lore\n      tags\n      type {\n        flatData {\n          slug\n          name\n          __typename\n        }\n        __typename\n      }\n      difficulty {\n        flatData {\n          slug\n          name\n          color\n          level\n          __typename\n        }\n        __typename\n      }\n      customDifficulty {\n        flatData {\n          slug\n          name\n          color\n          level\n          __typename\n        }\n        __typename\n      }\n      abilities {\n        flatData {\n          slug\n          name\n          activationKey\n          __typename\n        }\n        __typename\n      }\n      difficultyLevel\n      moderators {\n        flatData {\n          ...ModeratorFragment\n          __typename\n        }\n        __typename\n      }\n      damageType\n      playStyle\n      socialCommunities {\n        slug\n        url\n        __typename\n      }\n      preMobility\n      preToughness\n      preControl\n      preDamage\n      __typename\n    }\n    __typename\n  }\n  powerSpikesData: queryChampionsRoleDataV2Contents(filter: $allRolesDataFilter) {\n    flatData {\n      role\n      championSlug\n      gameStages {\n        gamePlan\n        gameStage\n        powerSpike\n        powerSpikeDescription\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  championAds: queryChampionsAdsV1Contents(filter: $championFilter) {\n    flatData {\n      ...LolChampionAdsFragment\n      __typename\n    }\n    __typename\n  }\n  buildGuide: queryLolChampionsExpertGuidesContents(filter: $expertGuideFilter) {\n    flatData {\n      ...ChampionExpertGuideFragment\n      __typename\n    }\n    __typename\n  }\n  seoOverride: queryChampionsSeoV1Contents(filter: $championFilter) {\n    flatData {\n      expertGuidePageTitle\n      expertGuidePageDesc\n      expertGuideOgImage\n      championExpertGuidesPageHeaderSeoText\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ModeratorFragment on ModeratorsV1DataFlatDto {\n  summonerName\n  region\n  rank\n  division\n  icon\n  links {\n    slug\n    link\n    __typename\n  }\n  shortBio\n  __typename\n}\n\nfragment LolChampionAdsFragment on ChampionsAdsV1DataFlatDto {\n  hBanner {\n    flatData {\n      alt\n      basePath\n      items {\n        maxWidth\n        prefix\n        x2Prefix\n        __typename\n      }\n      imgTrackingCode\n      linkUrl\n      slug\n      type\n      types\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChampionExpertGuideFragment on LolChampionsExpertGuidesDataFlatDto {\n  championSlug\n  championRoles\n  difficulty {\n    flatData {\n      slug\n      name\n      index\n      color\n      __typename\n    }\n    __typename\n  }\n  videoUrl\n  placeholderImage\n  expertVideoGuideTimestamps {\n    name\n    time\n    __typename\n  }\n  __typename\n}\n\"}"
    
    response = requests.post(url="https://mobalytics.gg/api/league/gql/static/v1",
                             data=body)
    return response.json()