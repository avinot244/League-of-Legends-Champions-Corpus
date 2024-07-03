from packages.utils.globals import DATASETS_PATH

from nltk import sent_tokenize, word_tokenize
import nltk
import json
from gensim.models.word2vec import Word2Vec

def prepare_dataset_w2v():
    nltk.download('punkt')
    tokenized_lines : list = list()
    with open(DATASETS_PATH + "fill-mask/train-lol-champs.jsonl") as file:
        for line in file:
            dataset : dict = json.loads(line)
            for k, v in dataset.items():
                sentence_tokenized : list = list()
                for sentence in sent_tokenize(v):
                    sentence_tokenized.append(word_tokenize(sentence))
                tokenized_lines += sentence_tokenized
            break
    return tokenized_lines

def train_model_w2v(model : Word2Vec, dataset : list):
    
    return 0