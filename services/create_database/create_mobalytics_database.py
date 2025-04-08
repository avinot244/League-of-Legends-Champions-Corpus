from packages.utils_func import replace_within_double_curly_brackets, get_token
from services.api.mobalytics.api_calls_mobalytics import *
from models.translation_augmentation import augment_data
from models.propositionizers import propositioner_llama
from packages.globals import DB_TYPES, DATASETS_PATH
from models.commons import labelize


from transformers.pipelines.text2text_generation import TranslationPipeline
from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5 import T5Tokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import transformers
from transformers import pipeline
import json
from tqdm import tqdm
import torch


def create_line(
    title : str, 
    text : str, 
    db_type : str, 
    buffer : list[str], 
    pipeline_en_fr : TranslationPipeline, 
    pipeline_fr_en : TranslationPipeline,
    to_labelize : bool = True
) -> list[str]:
    hf_read = get_token("read", "hf")
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_read)
    tokenizer.pad_token = tokenizer.eos_token
    
    assert db_type in DB_TYPES
    if to_labelize:
        new_text : str = labelize(replace_within_double_curly_brackets(text), title)
    else:
        new_text : str = replace_within_double_curly_brackets(text)
    
    if db_type == "fill-mask" or db_type == "w2v":               
        data : dict = {
            "label": title,
            "text": new_text,
        }
        buffer.append(data)

    elif db_type == "semantic-similarity":
        prop_list : list[str] = propositioner_llama(
            title, 
            "", 
            new_text
        )
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

def create_mobalytics_database(
    db_name : str,
    db_type : str
) -> None:
    assert db_type in DB_TYPES
    transformers.logging.set_verbosity_error()
    with open(DATASETS_PATH + "/champion_mapping.json", "r") as file:
        champion_names : list = json.load(file)

        champion_names = [s.lower() for s in champion_names]

        lines : list = []
        pipeline_en_fr : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
        pipeline_fr_en : TranslationPipeline= pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
        
        model_name = "chentong00/propositionizer-wiki-flan-t5-large"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
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
                        to_labelize=False
                    )
                
                # For champMU data
                lines = create_line(
                    champion_name, 
                    champMUData["flatData"]["matchupTips"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en,
                )

                # For Strenght and weaknesses
                lines = create_line(
                    champion_name, 
                    snwData["flatData"]["strengths"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en
                )
                lines = create_line(
                    champion_name, 
                    snwData["flatData"]["weaknesses"], 
                    db_type, 
                    lines, 
                    pipeline_en_fr, 
                    pipeline_fr_en
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
                        pipeline_fr_en
                    )
                    lines = create_line(
                        champion_name, 
                        pwGS["powerSpikeDescription"], 
                        db_type, 
                        lines, 
                        pipeline_en_fr, 
                        pipeline_fr_en
                    )
                
                with open(DATASETS_PATH + f"/{db_type}/{db_name}.jsonl", "a") as f:
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
                                    "label": label,
                                    "text": current_chunk.strip(),
                                }
                                current_chunk = line["text"]
                                f.write(json.dumps(data) + "\n")
                        if current_chunk:
                            data : dict = {
                                "label": label,
                                "text": current_chunk.strip(),
                            }
                            f.write(json.dumps(data) + "\n")
                                