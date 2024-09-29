from packages.utils.utils_func import replace_within_double_curly_brackets
from packages.db_manager.mobalytics.api_calls_mobalytics import *
from packages.models.translation_augmentation import augment_data
from packages.utils.globals import DB_TYPES, DATASETS_PATH
from packages.db_manager.youtube.api_calls_youtube import get_playlist_videos, get_playlist_id, download_audio
from packages.utils.utils_func import get_token
from packages.commons import propositionizer, propositioner_llama


from transformers.pipelines.text2text_generation import TranslationPipeline
from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5_fast import T5TokenizerFast
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import transformers
from datasets import load_dataset
from transformers import pipeline
import json
from tqdm import tqdm
import numpy as np
import torch
import os

def create_line(
    title : str, 
    text : str, 
    db_type : str, 
    buffer : list[str], 
    pipeline_en_fr : TranslationPipeline, 
    pipeline_fr_en : TranslationPipeline,
    model : T5ForConditionalGeneration,
    tokenizer : T5TokenizerFast,
    device : str
) -> list[str]:
    
    assert db_type in DB_TYPES
    new_text : str = replace_within_double_curly_brackets(text)
    prop_list : list[str] = propositioner_llama(
        title, 
        "", 
        new_text
    )
    if db_type == "fill-mask" or db_type == "w2v":        
        for prop in prop_list:
            data : dict = {
                "label": title,
                "text": prop
            }
            data_bis : dict = {
                "label": title,
                "text": augment_data(prop, pipeline_en_fr, pipeline_fr_en)
            }
            buffer.append(data)
            buffer.append(data_bis)

    elif db_type == "semantic-similarity":
        for prop in prop_list:
            data : dict = {
                "label": title,
                "set" : [
                    prop,
                    augment_data(prop, pipeline_en_fr, pipeline_fr_en)
                ]
            }
        buffer.append(data)
        
    return buffer

def create_mobalytics_dataset(
    db_name : str,
    db_type : str
) -> None:
    assert db_type in DB_TYPES
    transformers.logging.set_verbosity_error()
    with open(DATASETS_PATH + "champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)

        champion_names : list[str] = list(champion_mapping.keys())

        champion_names = [s.lower() for s in champion_names]

        lines : list = []
        pipeline_en_fr : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
        pipeline_fr_en : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
        
        model_name = "chentong00/propositionizer-wiki-flan-t5-large"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        
        for champion_name in tqdm(champion_names):
            snw : dict = get_champion_SnW(champion_name)
            snwDataList : list = snw["data"]["guidesByRoleData"]
            
            powerSpikes : dict = get_champion_powerSpikes(champion_name)
            powerSpikesDataList : list = powerSpikes["data"]["powerSpikesData"]

            counters : dict = get_champion_counters(champion_name)
            champMU : list = counters["data"]["championMatchupSpecificData"]
            champRole : list = counters["data"]["championRoleData"]

            
            for pwData, snwData, champMUData, champRoleData in zip(powerSpikesDataList, snwDataList, champMU, champRole):
                # print("Counter match up tips")
                # For counter match up tips
                champRoleDataList : list = champRoleData["flatData"]["counterTips"]
                for counterTips in champRoleDataList:
                    lines = create_line(
                        f"Against {champion_name}",
                        counterTips["text"], 
                        db_type, 
                        lines, 
                        pipeline_en_fr, 
                        pipeline_fr_en,
                        model,
                        tokenizer,
                        device
                    )
                
                # For champMU data
                # print("Match up")
                lines = create_line(
                    champion_name, 
                    champMUData["flatData"]["matchupTips"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en,
                    model,
                    tokenizer,
                    device
                )

                # print("Strenghts and weaknesses")
                # For Strenght and weaknesses
                lines = create_line(
                    champion_name, 
                    snwData["flatData"]["strengths"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en,
                    model,
                    tokenizer,
                    device
                )
                lines = create_line(
                    champion_name, 
                    snwData["flatData"]["weaknesses"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en,
                    model,
                    tokenizer,
                    device
                )
                
                # print("Power Spikes")
                # For Power spikes
                pwGameStages = pwData["flatData"]["gameStages"]
                for pwGS in pwGameStages:
                    lines = create_line(
                        champion_name, 
                        pwGS["gamePlan"], 
                        db_type, 
                        lines, 
                        pipeline_en_fr, 
                        pipeline_fr_en,
                        model,
                        tokenizer,
                        device
                    )
                    lines = create_line(
                        champion_name, 
                        pwGS["powerSpikeDescription"], 
                        db_type, 
                        lines, 
                        pipeline_en_fr, 
                        pipeline_fr_en,
                        model,
                        tokenizer,
                        device
                    )
                
                with open(DATASETS_PATH + f"{db_type}/{db_name}.jsonl", "w") as f:
                    for line in lines:
                        f.write(json.dumps(line) + "\n")
        
        # db_size = len(lines)
        # train_size = round(db_size * 0.80)

        # np.random.shuffle(lines)
        # train_data = lines[:train_size]
        # test_data = lines[train_size + 1:]

        # with open(DATASETS_PATH + "{}/train-{}.jsonl".format(db_type, db_name), "w") as f:
        #     for line in train_data:
        #         f.write(json.dumps(line) + "\n")

        # with open(DATASETS_PATH + "{}/test-{}.jsonl".format(db_type, db_name), "w") as f:
        #     for line in test_data:
        #         f.write(json.dumps(line) + "\n")

def get_mp3_files():
    # https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69
    playlist_id : str = get_playlist_id("https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69")
    url_list : list[str] = get_playlist_videos(playlist_id)[:-3]
    
    for url in url_list:
        download_audio(url, DATASETS_PATH + "/youtube")

def create_youtube_dataset():
    transformers.logging.set_verbosity_error()
    hf_read = get_token("read")
    
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        chunk_length_s=30,
        device=device
    )
    
    ds = load_dataset("avinot/LoL-Champion-Guides-audio", token=hf_read, split="train")
    
    for line in tqdm(ds, position=0):
        sample = line["audio"]
        label = line["label"]
        id = line["id"]
        
        
        
        prediction = pipe(sample.copy(), batch_size=8)
        
        print(label)
        text_list : list[str] = propositioner_llama(
            label, 
            "", 
            prediction["text"]
        )
        
        for text in text_list:
            data : dict = {
                "text": text,
                "label": label,
                "id": id, 
            }
            if not(os.path.exists(DATASETS_PATH + "youtube/text/all-champs.jsonl")):
                option = "w"
            else:
                option = "a+"
            with open(DATASETS_PATH + "youtube/text/all-champs.jsonl", option) as f:
                json.dump(data, f)
                f.write("\n")
