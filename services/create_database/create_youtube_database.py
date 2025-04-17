from services.api.mobalytics.api_calls_mobalytics import *
from packages.globals import DB_TYPES, DATASETS_PATH
from services.api.youtube.api_calls_youtube import get_playlist_videos, get_playlist_id, download_audio
from packages.utils_func import get_token
from models.commons import labelize

from transformers import AutoTokenizer
import transformers
from datasets import load_dataset
from transformers import pipeline
from tqdm import tqdm
import torch
import os

def get_mp3_files(playlist_link : str):
    playlist_id : str = get_playlist_id(playlist_link)
    url_list : list[str] = get_playlist_videos(playlist_id)[:-3]
    
    for url in url_list:
        download_audio(url, DATASETS_PATH + "/youtube/audio")


def create_youtube_database():
    # Set logging verbosity
    transformers.logging.set_verbosity_error()
    hf_read = get_token("read", "hf")

    # Set device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Initialize the pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        chunk_length_s=15,
        device=device
    )

    # Load the dataset
    ds = load_dataset("avinot/LoL-Champion-Guides-audio", token=hf_read, split="train")

    # Load the tokenizer
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_read)
    tokenizer.pad_token = tokenizer.eos_token
    output_path = DATASETS_PATH + "/youtube/text/all-champs.jsonl"
    
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
        id_list = [d["id"] for d in data]
    else:
        id_list = []
    
    # Labelize each chunk if the label is a champion
    champion_list : list[str] = list()
    with open("./data/champion_mapping.json", "r") as f:
        champion_list = json.load(f)
        champion_list = [c.lower() for c in champion_list]
    
    # Get a sample from the dataset
    for line in tqdm(ds, position=0):
        sample = line["audio"]
        label : str = line["label"]
        id = line["id"]
        if not(id in id_list):
            # Transcribe the audio sample
            try:
                with torch.no_grad():
                    prediction = pipe(sample.copy(), batch_size=1)
                transcribed_text = prediction["text"]
            except Exception as e:
                print(f"[ERROR] Transcription failed for id {id}: {e}")
                continue  # skip to the next sample
            
            if label.lower() in champion_list:
                labeled_transcription = labelize(transcribed_text, label)
            else:
                labeled_transcription = transcribed_text
            
            # Save the labeled chunks to a JSONL file
            with open(output_path, "a") as f:
                f.write(f'{{"id": "{id}", "label": "{label}", "text": "{labeled_transcription}"}}\n')
            
            del prediction
            del sample
            torch.cuda.empty_cache()

