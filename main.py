from src.create_database import create_semantic_classification_dataset
from src.create_word_embedding import create_bert_word_embedding, create_word2vec_word_embedding
import numpy
import json
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-classification", action="store_true", default=False, help="Create database for semantic classifiction")
    parser.add_argument("--create-word-embedding", metavar="[BERT/Word2Vec]", type=str, help="Create word embedding model from our dataset")
    args = parser.parse_args()
    args_data = vars(args)
       
    if args_data["create_db_classification"]:
        create_semantic_classification_dataset()
    elif args_data["create_word_embedding"] == "BERT":
        create_bert_word_embedding()
    elif args_data["create_word_embedding"] == "Word2Vec":
       create_word2vec_word_embedding()