from services.api.mobalytics.api_calls_mobalytics import *
from packages.globals import DB_TYPES, DATASETS_PATH
from services.api.youtube.api_calls_youtube import get_playlist_videos, get_playlist_id, download_audio
from packages.utils_func import get_token
from models.propositionizers import propositionizer
from models.commons import chunk_text

from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5 import T5Tokenizer
from transformers import AutoTokenizer
import transformers
from datasets import load_dataset
from transformers import pipeline
from tqdm import tqdm
import torch

def get_mp3_files():
    # https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69
    playlist_id : str = get_playlist_id("https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=lDKE3JfRxGRBVE69")
    url_list : list[str] = get_playlist_videos(playlist_id)[:-3]
    
    for url in url_list:
        download_audio(url, DATASETS_PATH + "/youtube")


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

