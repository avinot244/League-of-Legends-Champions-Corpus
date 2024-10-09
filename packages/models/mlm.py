import os
import torch
from transformers import BertTokenizer, BertForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Load the dataset
dataset = load_dataset('avinot/LoL-Champions-Corpus')

# Load the pre-trained BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

# Data Collator for MLM (this will handle masking the tokens during training)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15
)

# Load the pre-trained BERT model
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# Define training arguments
training_args = TrainingArguments(
    output_dir='./bert-mlm-lol-champions',   # directory to save the model
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=8,   # Adjust based on your GPU memory
    per_device_eval_batch_size=8,
    evaluation_strategy="steps",    # Evaluate at every N steps
    logging_dir='./logs',           # Directory for logging
    logging_steps=500,
    save_steps=1000,
    eval_steps=1000,
    save_total_limit=2,             # Only last 2 checkpoints will be saved
    prediction_loss_only=True,      # Simplifies output for MLM task
    learning_rate=5e-5,
)

# Define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],   # Assuming dataset has 'test' split
    data_collator=data_collator,
)

# Fine-tune the model
trainer.train()

# Save the final model
model.save_pretrained('./bert-mlm-lol-champions-final')
tokenizer.save_pretrained('./bert-mlm-lol-champions-final')
