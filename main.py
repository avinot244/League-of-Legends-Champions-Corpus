from packages.model import *
from packages.utils import saveToJson
from packages.api_calls import get_champion_SnW, get_champion_powerSpikes


import os
import json

if __name__ == "__main__":


    with open("./champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)

    champion_names : list[str] = list(champion_mapping.keys())

    champion_names = [s.lower() for s in champion_names]
    
    test = champion_names[-1]
    snw : dict = get_champion_SnW(test)
    snwDataList : list = snw["data"]["guidesByRoleData"]
    
    powerSpikes : dict = get_champion_powerSpikes(test)
    powerSpikesDataList : list = powerSpikes["data"]["powerSpikesData"]

    row_idx : int = 0
    for pwData, snwData in zip(powerSpikesDataList, snwDataList):
        # For Strenght and weaknesses
        rowContentS : RowContent = RowContent(snwData["flatData"]["strengths"], -1)
        rowS : Row = Row(row_idx, rowContentS)
        row_idx += 1
        saveToJson(rowS.asDict(), "./dataset.json")

        rowContentW : RowContent = RowContent(snwData["flatData"]["weaknesses"], -1)
        rowW : Row = Row(row_idx, rowContentW)
        row_idx += 1
        saveToJson(rowW.asDict(), "./dataset.json")
        
        
        # For Power spikes
        pwGameStages = pwData["flatData"]["gameStages"]
        for pwGS in pwGameStages:
            
            rowContentGamePlan : RowContent = RowContent(pwGS["gamePlan"], -1)
            rowGamePlan : Row = Row(row_idx, rowContentGamePlan)
            row_idx += 1
            saveToJson(rowGamePlan.asDict(), "./dataset.json")

            rowContentDescription : RowContent = RowContent(pwGS["powerSpikeDescription"], -1)
            rowDescription : Row = Row(row_idx, rowContentDescription)
            row_idx += 1           
            saveToJson(rowDescription.asDict(), "./dataset.json")
            


            






