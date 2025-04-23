from transformers import AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

# Load the tokenizer for the llama-3.2-1B model
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")

# Load the dataset
dataset = load_dataset("avinot/LoL-Corpus-v4", split="train")

# Function to count tokens in the dataset
def count_tokens(dataset, tokenizer):
    total_tokens = 0
    for example in tqdm(dataset):
        text = example["text"]  # Adjust the key based on your dataset
        tokens = tokenizer.encode(text, add_special_tokens=True)
        total_tokens += len(tokens)
    return total_tokens

# Count tokens in the train split
total_tokens = count_tokens(dataset, tokenizer)
print(f"Total tokens in the train split: {total_tokens}")