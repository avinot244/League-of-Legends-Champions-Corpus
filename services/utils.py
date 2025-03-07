from transformers import pipeline
from datasets import load_dataset
import transformers
import torch
import json
from tqdm import tqdm
from transformers import AutoTokenizer

from models.propositionizers import propositioner_llama
from packages.utils_func import get_token
from models.commons import chunk_text

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
                