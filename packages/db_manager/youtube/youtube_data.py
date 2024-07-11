from datasets import Dataset
import datasets
import os
import uuid

from packages.utils.globals import DATASETS_PATH
from packages.utils.utils_func import get_token



def push_audio_dataset():
    audio_dataset_dict = {
        "audio": [],
        "label": [],
        "id": []
    }
    for root, dirs, files in os.walk(DATASETS_PATH + "youtube/audio/"):
        for name in files:
            audio_dataset_dict["audio"].append(os.path.join(root, name))
            audio_dataset_dict["label"].append(name.split(' ')[2])
            audio_dataset_dict["id"].append(str(uuid.uuid4()))
            
    
    audio_dataset = Dataset.from_dict(audio_dataset_dict).cast_column("audio", datasets.Audio(sampling_rate=16000))
    hf_key = get_token(option="write")
    audio_dataset.push_to_hub("avinot/LoL-Champion-Guides-audio", token=hf_key)
    