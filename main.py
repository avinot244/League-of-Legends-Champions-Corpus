from src.create_database import create_semantic_classification_dataset
from src.create_word_embedding import create_word_embedding, getWordSimilarity, clusteringChamps
import numpy
import json
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-classification", action="store_true", default=False, help="Create database for semantic classifiction")
    parser.add_argument("--create-word-embedding", action="store_true", default=False, help="Create word embedding model from our dataset")
    parser.add_argument("--get-similarity", action="store_true", default=False, help="Get similarity of two words")
    parser.add_argument("--clustering", action="store_true", default=False, help="Clustering of champions")
    args = parser.parse_args()
    args_data = vars(args)
       
    if args_data["create_db_classification"]:
        create_semantic_classification_dataset()
    elif args_data["create_word_embedding"]:
        create_word_embedding()
    elif args_data["get_similarity"]:
        getWordSimilarity("Orianna", "Azir")
        getWordSimilarity("Orianna", "Car")
        getWordSimilarity("Orianna", "Arianna")
        getWordSimilarity("Ornn", "Zac")
    elif args_data["clustering"]:
        clusteringChamps()