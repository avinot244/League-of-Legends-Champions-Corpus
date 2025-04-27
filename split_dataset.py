import math
import random
import json
from transformers import AutoTokenizer

#80% : train
#20% : validation

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B", legacy=False)

# File paths
input_file = "./data/fill-mask/v6/lol-champs.jsonl"
train_file = "./data/fill-mask/v6/lol-champs-train.jsonl"
val_file = "./data/fill-mask/v6/lol-champs-validation.jsonl"

# Read the input file
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Shuffle the lines
random.shuffle(lines)

# Count the total number of tokens in the input file
total_tokens = sum(len(tokenizer.tokenize(json.loads(line)["text"])) for line in lines)

# Compute the token thresholds for training and validation sets
train_token_threshold = math.floor(0.8 * total_tokens)
train_tokens = 0

# Split the lines into training and validation sets
train_lines = []
val_lines = []

for line in lines:
    line_tokens = len(tokenizer.tokenize(json.loads(line)["text"]))
    if train_tokens + line_tokens <= train_token_threshold:
        train_lines.append(line)
        train_tokens += line_tokens
    else:
        val_lines.append(line)

# Write the training set to the train file
with open(train_file, "w", encoding="utf-8") as f:
    f.writelines(train_lines)

# Write the validation set to the validation file
with open(val_file, "w", encoding="utf-8") as f:
    f.writelines(val_lines)
