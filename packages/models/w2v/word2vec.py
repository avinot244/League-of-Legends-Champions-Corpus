from packages.utils.globals import DATASETS_PATH

from nltk import sent_tokenize, word_tokenize
import nltk
import json
from gensim.models.word2vec import Word2Vec
from tqdm import tqdm
import pandas as pd
import re

def prepare_dataset_w2v():
    nltk.download('punkt')
    tokenized_lines : list = list()
    with open(DATASETS_PATH + "w2v/train-lol-champs-w2v.jsonl") as file:
        for line in file:
            dataset : dict = json.loads(line)
            for k, v in dataset.items():
                sentence_tokenized : list = list()
                for sentence in sent_tokenize(v):
                    sentence_tokenized.append(word_tokenize(sentence.lower()))
                tokenized_lines += sentence_tokenized
    return tokenized_lines

def train_model_w2v(model : Word2Vec, dataset : list):
    model.build_vocab(dataset)
    total_examples : int = model.corpus_count
    vocab = list(model.wv.key_to_index.keys())
    model.train(dataset, total_examples=total_examples, epochs=model.epochs)
    return model, vocab