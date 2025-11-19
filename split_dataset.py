import random

input_path = "./data/contrastive/v5/champion_triplets_rationales.jsonl"
train_path = "./data/contrastive/v5/champion_triplets_rationales_train.jsonl"
val_path = "./data/contrastive/v5/champion_triplets_rationales_val.jsonl"
split_ratio = 0.8  # 80% train, 20% val

# Read all lines
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

random.shuffle(lines)
split_idx = int(len(lines) * split_ratio)
train_lines = lines[:split_idx]
val_lines = lines[split_idx:]

with open(train_path, "w", encoding="utf-8") as f:
    f.writelines(train_lines)
    
with open(val_path, "w", encoding="utf-8") as f:
    f.writelines(val_lines)
