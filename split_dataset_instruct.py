import math
import random
import json
from transformers import AutoTokenizer
from tqdm import tqdm

#80% : train
#20% : validation

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B", legacy=False)

input_file = "./data/instruct/v2/lol-instruct.jsonl"
train_file = "./data/instruct/v2/lol-instruct-train.jsonl"
validation_file = "./data/instruct/v2/lol-instruct-validation.jsonl"

# Read the input file
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Shuffle the lines
random.shuffle(lines)

# Count the total number of tokens in the input file
total_tokens = sum(len(tokenizer.tokenize(json.loads(line)["messages"][-1]["content"])) for line in lines)

# Compute the token thresholds for training and validation sets
train_token_threshold = math.floor(0.8 * total_tokens)
train_tokens = 0

# Split the lines into training and validation sets
train_lines = []
val_lines = []

for line in tqdm(lines):
    line_tokens = len(tokenizer.tokenize(json.loads(line)["messages"][-1]["content"]))
    if train_tokens + line_tokens <= train_token_threshold:
        train_lines.append(line)
        train_tokens += line_tokens
    else:
        val_lines.append(line)

# Write the training set to the train file
with open(train_file, "w", encoding="utf-8") as f:
    f.writelines(train_lines)

# Write the validation set to the validation file
with open(validation_file, "w", encoding="utf-8") as f:
    f.writelines(val_lines)

