from packages.utils.utils_func import replace_within_double_curly_brackets
from packages.db_manager.mobalytics.api_calls_mobalytics import *
from packages.models.translation_augmentation import augment_data
from packages.utils.globals import DB_TYPES, DATASETS_PATH

from transformers.pipelines.text2text_generation import TranslationPipeline

from transformers import pipeline
import json
from tqdm import tqdm
import numpy as np

def create_line(text : str, champion_name : str, context : str, db_type : str, buffer : list, pipeline_en_fr : TranslationPipeline, pipeline_fr_en : TranslationPipeline):
    assert db_type in DB_TYPES
    if db_type == "fill-mask":
        data : dict = {
            "text" : "{} {}, {}".format(context, champion_name, replace_within_double_curly_brackets(text))
        }
        buffer.append(data)
        
        data_bis : dict = {
            "text" : "{} {}, {}".format(context, champion_name, augment_data(replace_within_double_curly_brackets(text), pipeline_en_fr, pipeline_fr_en))
        }
        buffer.append(data_bis)
        
    elif db_type == "semantic-similarity":
        data : dict = {
            "set" : [
                "{} {}, {}".format(context, champion_name, replace_within_double_curly_brackets(text)),
                "{} {}, {}".format(context, champion_name, augment_data(replace_within_double_curly_brackets(text)), pipeline_en_fr, pipeline_fr_en),
            ]
        }
        buffer.append(data)
        
    elif db_type == "w2v":
        data : dict = {
            "text" : "{} {}, {}".format(context, champion_name, replace_within_double_curly_brackets(text))
        }
        buffer.append(data)
        
        data_bis : dict = {
            "text" : "{} {}, {}".format(context, champion_name, augment_data(replace_within_double_curly_brackets(text), pipeline_en_fr, pipeline_fr_en))
        }
        buffer.append(data_bis)
        
    return buffer

def create_mobalytics_dataset(db_name : str, db_type : str):
    assert db_type in DB_TYPES
    with open(DATASETS_PATH + "champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)

        champion_names : list[str] = list(champion_mapping.keys())

        champion_names = [s.lower() for s in champion_names]

        lines : list = []
        pipeline_en_fr : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
        pipeline_fr_en : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
        print(type(pipeline_fr_en))
        for champion_name in tqdm(champion_names):
            snw : dict = get_champion_SnW(champion_name)
            snwDataList : list = snw["data"]["guidesByRoleData"]
            
            powerSpikes : dict = get_champion_powerSpikes(champion_name)
            powerSpikesDataList : list = powerSpikes["data"]["powerSpikesData"]

            counters : dict = get_champion_counters(champion_name)
            champMU : list = counters["data"]["championMatchupSpecificData"]
            champRole : list = counters["data"]["championRoleData"]

            
            for pwData, snwData, champMUData, champRoleData in zip(powerSpikesDataList, snwDataList, champMU, champRole):
                # For counter match up tips
                champRoleDataList : list = champRoleData["flatData"]["counterTips"]
                for counterTips in champRoleDataList:
                    lines = create_line(counterTips["text"], champion_name, "Against", db_type, lines, pipeline_en_fr, pipeline_fr_en)
                
                # For champMU data
                lines = create_line(champMUData["flatData"]["matchupTips"], champion_name, "As", db_type, lines, pipeline_en_fr, pipeline_fr_en)

                # For Strenght and weaknesses
                lines = create_line(snwData["flatData"]["strengths"], champion_name, "As", db_type, lines, pipeline_en_fr, pipeline_fr_en)
                lines = create_line(snwData["flatData"]["weaknesses"], champion_name, "As", db_type, lines, pipeline_en_fr, pipeline_fr_en)
                
                # For Power spikes
                pwGameStages = pwData["flatData"]["gameStages"]
                for pwGS in pwGameStages:
                    lines = create_line(pwGS["gamePlan"], champion_name, "As", db_type, lines, pipeline_en_fr, pipeline_fr_en)
                    lines = create_line(pwGS["powerSpikeDescription"], champion_name, "As", db_type, lines, pipeline_en_fr, pipeline_fr_en)
        db_size = len(lines)
        train_size = round(db_size * 0.80)

        np.random.shuffle(lines)
        train_data = lines[:train_size]
        test_data = lines[train_size + 1:]

        with open(DATASETS_PATH + "{}/train-{}.jsonl".format(db_type, db_name), "w") as f:
            for line in train_data:
                f.write(json.dumps(line) + "\n")

        with open(DATASETS_PATH + "{}/test-{}.jsonl".format(db_type, db_name), "w") as f:
            for line in test_data:
                f.write(json.dumps(line) + "\n")


