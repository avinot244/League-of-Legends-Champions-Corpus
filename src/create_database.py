from packages.utils.utils_func import replace_within_double_curly_brackets
from packages.db_manager.mobalytics.api_calls_mobalytics import *
from packages.models.translation_augmentation import augment_data
from packages.utils.globals import DB_TYPES, DATASETS_PATH
from packages.db_manager.youtube.api_calls_youtube import get_playlist_videos, get_playlist_id, download_audio
from packages.utils.utils_func import get_token
from packages.commons import propositionizer, propositioner_llama


from transformers.pipelines.text2text_generation import TranslationPipeline
from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5 import T5Tokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import transformers
from datasets import load_dataset
from transformers import pipeline
import json
from tqdm import tqdm
import numpy as np
import torch
import os
import re

def labelize(text : str, label : str):
    replacements = {
        r"\bhe\b": f"{label}",
        r"\bshe\b": f"{label}",
        r"\byou\b": f"{label}",
        r"\bhis\b": f"{label}'s",
        r"\bher\b": f"{label}'s"
    }
    
    for key, value in replacements.items():
        text = re.sub(key, value, text, flags=re.IGNORECASE)
    
    return text

def chunk_text(id : str, propositions : list[str], label : str, tokenizer : AutoTokenizer):
    chunk_texts = []
    current_chunk = ""
    for proposition in propositions:
        labeled_proposition = labelize(proposition, label)
        tokenized_proposition = tokenizer.tokenize(labeled_proposition)
        if len(tokenizer.tokenize(current_chunk)) + len(tokenized_proposition) <= 512:
            current_chunk += " " + labeled_proposition
        else:
            chunk_texts.append(current_chunk.strip())
            data : dict = {
                "text": current_chunk.strip(),
                "label": label,
                "id": id
            }
            if not(os.path.exists(DATASETS_PATH + "youtube/text/all-champs.jsonl")):
                option = "w"
            else:
                option = "a+"
            with open(DATASETS_PATH + "youtube/text/all-champs.jsonl", option) as f:
                json.dump(data, f)
                f.write("\n")
            
            current_chunk = labeled_proposition
    if current_chunk != "":
        data : dict = {
            "text": current_chunk.strip(),
            "label": label,
            "id": id
        }
        if not(os.path.exists(DATASETS_PATH + "youtube/text/all-champs.jsonl")):
            option = "w"
        else:
            option = "a+"
        with open(DATASETS_PATH + "youtube/text/all-champs.jsonl", option) as f:
            json.dump(data, f)
            f.write("\n")

def create_line(
    title : str, 
    text : str, 
    db_type : str, 
    buffer : list[str], 
    pipeline_en_fr : TranslationPipeline, 
    pipeline_fr_en : TranslationPipeline,
    model : T5ForConditionalGeneration,
    tokenizer : T5Tokenizer,
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
        champion_names : list = json.load(file)

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
            
            valid_data = zip(
                powerSpikesDataList if powerSpikesDataList is not None else [],
                snwDataList if snwDataList is not None else [],
                champMU if champMU is not None else [],
                champRole if champRole is not None else []
            )
            for pwData, snwData, champMUData, champRoleData in valid_data:
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
                
                with open(DATASETS_PATH + f"{db_type}/{db_name}.jsonl", "a") as f:
                    label_chunks = {}
                    for line in lines:
                        label = line["label"]
                        if label not in label_chunks:
                            label_chunks[label] = []
                        label_chunks[label].append(line)
                    
                    for label, lines in label_chunks.items():
                        chunk_texts = []
                        current_chunk = ""
                        for line in lines:
                            tokenized_proposition = tokenizer.tokenize(line["text"])
                            if len(tokenizer.tokenize(current_chunk)) + len(tokenized_proposition) <= 512:
                                current_chunk += " " + line["text"]
                            else:
                                chunk_texts.append(current_chunk.strip())
                                data : dict = {
                                    "text": current_chunk.strip(),
                                    "label": label,
                                }
                                current_chunk = line["text"]
                                f.write(json.dumps(data) + "\n")
                        if current_chunk:
                            data : dict = {
                                "text": current_chunk.strip(),
                                "label": label,
                            }
                            f.write(json.dumps(data) + "\n")
                                


def get_mp3_files():
    # https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69
    playlist_id : str = get_playlist_id("https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69")
    url_list : list[str] = get_playlist_videos(playlist_id)[:-3]
    
    for url in url_list:
        download_audio(url, DATASETS_PATH + "/youtube")


def create_youtube_dataset():
    # Set logging verbosity
    transformers.logging.set_verbosity_error()
    hf_read = get_token("read")

    # Set device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Initialize the pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        chunk_length_s=30,
        device=device
    )

    # Load the dataset
    ds = load_dataset("avinot/LoL-Champion-Guides-audio", token=hf_read, split="train")

    # Load the tokenizer
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_read)
    tokenizer.pad_token = tokenizer.eos_token
    
    model_name_prop = "chentong00/propositionizer-wiki-flan-t5-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer_prop = T5Tokenizer.from_pretrained(model_name_prop)
    model = T5ForConditionalGeneration.from_pretrained(model_name_prop).to(device)

    # Get a sample from the dataset
    for line in tqdm(ds, position=0):
        sample = line["audio"]
        label = line["label"]
        id = line["id"]

        # Transcribe the audio sample
        prediction = pipe(sample.copy(), batch_size=8)
        transcribed_text = prediction["text"]

        # Tansform the text into propositions
        propositions : list[str] = propositionizer(id, label, "", transcribed_text, model, tokenizer_prop, device)
        chunk_text(propositions, label, tokenizer)

def regenerate_error_lines():
    transformers.logging.set_verbosity_error()
    hf_read = get_token("read")

    # Set device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Initialize the pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        chunk_length_s=30,
        device=device
    )

    # Load the dataset
    ds = load_dataset("avinot/LoL-Champion-Guides-audio", token=hf_read, split="train")

    # Load the tokenizer
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_read)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Get the list of line that are in error
    error_data : dict = {}
    with open("error_propositionizer.json", "r") as f:
        error_data : dict = json.load(f)
    
    for error_sample in tqdm(error_data["error"]):
        # Get the wanted sample of the right ID from the audio dataset
        for line in ds:
            if line["id"] == error_sample["id"]:
                sample = line["audio"]
                label = line["label"]
                id = line["id"]

                # Transcribe the audio sample
                prediction = pipe(sample.copy(), batch_size=8)
                transcribed_text = prediction["text"]

                # Tansform the text into propositions
                propositions : list[str] = propositioner_llama(label, "", transcribed_text)
                chunk_text(id, propositions, label, tokenizer)
                