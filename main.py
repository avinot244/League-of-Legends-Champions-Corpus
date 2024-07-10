from src.create_database import create_mobalytics_dataset, create_youtube_dataset
from src.create_word_embedding import create_bert_word_embedding, create_word2vec_word_embedding
from packages.utils.globals import DATASETS_PATH

import numpy
import json
import argparse
from gensim.models.keyedvectors import KeyedVectors
import uuid
from sklearn.cluster import KMeans

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-mobalytics", action="store_true", default=False, help="Create database from mobalytics")
    parser.add_argument("--create-db-youtube", action="store_true", default=False, help="Creat database from youtube")
    parser.add_argument("--db-type", metavar="[str]", type=str, help="Tells wich type of database you want to create")
    parser.add_argument("--db-name", metavar="[str]", type=str, help="Name of database")
    parser.add_argument("--word-embedding", metavar="[BERT/Word2Vec]", type=str, help="Create word embedding model from our dataset")
    parser.add_argument("--load-word-embedding", metavar="[uuid]", type=str, help="Load a give w2v model")
    args = parser.parse_args()
    args_data = vars(args)
       
    if args_data["create_db_mobalytics"]:
        db_name : str = args_data["db_name"]
        db_type : str = args_data["db_type"]
        assert db_type != None
        assert db_name != None
        create_mobalytics_dataset(db_name, db_type)
        
    elif args_data["create_db_youtube"]:
        create_youtube_dataset()
        
    elif args_data["word_embedding"] == "BERT":
        create_bert_word_embedding()
        
    elif args_data["word_embedding"] == "Word2Vec":
        vocab : list = list()
        wv : KeyedVectors = None
        if args_data["load_word_embedding"] == None:
            (vocab, wv) = create_word2vec_word_embedding()
            wv.save_word2vec_format("./models/w2v/w2v_{}.kv".format(uuid.uuid4()))
        else:
            wv = KeyedVectors.load_word2vec_format("./models/w2v/w2v_{}.kv".format(args_data["load_word_embedding"]))
        
        # Getting champion list
        champion_names : list[str] = list()
        with open("./datasets/champion_mapping.json", "r") as file:
            champion_mapping : dict = json.load(file)
            champion_names = [s.lower() for s in list(champion_mapping.keys())]
        
        print("Most similar words for orianna:")
        for w, sim in wv.most_similar(positive=["orianna"]):
            print((w, sim))
        
        print("\n------\n")
        
        