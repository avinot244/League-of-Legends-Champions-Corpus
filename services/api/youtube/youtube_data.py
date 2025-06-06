from datasets import Dataset
import datasets
import os
import uuid
import json
from tqdm import tqdm

from packages.globals import DATASETS_PATH
from packages.utils_func import get_token



def push_audio_dataset():
    champion_list : list[str] = list()
    with open(DATASETS_PATH + "/champion_mapping.json", "r") as f:
        champion_list = json.load(f)
    
    audio_dataset_dict = {
        "audio": [],
        "label": [],
        "id": []
    }
    for root, dirs, files in os.walk(DATASETS_PATH + "/youtube/audio/"):
        name : str
        for name in tqdm(files):
            label : str = ""
            for champion in champion_list:
                if champion.lower() in name.lower():
                    label = champion.lower()
                    
            if label == "":
                label = name
            audio_dataset_dict["audio"].append(os.path.join(root, name))
            audio_dataset_dict["label"].append(label)
            audio_dataset_dict["id"].append(str(uuid.uuid4()))
            
    print(audio_dataset_dict)
    audio_dataset = Dataset.from_dict(audio_dataset_dict).cast_column("audio", datasets.Audio(sampling_rate=16000))
    hf_key = get_token(type="hf", option="write")
    audio_dataset.push_to_hub("avinot/LoL-Champion-Guides-audio", token=hf_key)
    