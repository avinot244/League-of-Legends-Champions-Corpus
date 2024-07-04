from src.create_database import create_mobalytics_dataset
from src.create_word_embedding import create_bert_word_embedding, create_word2vec_word_embedding

import numpy
import json
import argparse
from gensim.models.keyedvectors import KeyedVectors

def temp(lst : list):
    lst.append(99)
    return lst

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-mobalytics", action="store_true", default=False, help="Create database from mobalytics")
    parser.add_argument("--db-type", metavar="[str]", type=str, help="Tells wich type of database you want to create")
    parser.add_argument("--db-name", metavar="[str]", type=str, help="Name of database")
    parser.add_argument("--create-word-embedding", metavar="[BERT/Word2Vec]", type=str, help="Create word embedding model from our dataset")
    args = parser.parse_args()
    args_data = vars(args)
    
       
    if args_data["create_db_mobalytics"]:
        
        db_name : str = args_data["db_name"]
        db_type : str = args_data["db_type"]
        assert db_type != None
        assert db_name != None
        create_mobalytics_dataset(db_name, db_type)
    elif args_data["create_word_embedding"] == "BERT":
        create_bert_word_embedding()
    elif args_data["create_word_embedding"] == "Word2Vec":
        vocab : list = list()
        wv : KeyedVectors = None
        (vocab, wv) = create_word2vec_word_embedding()
        wv.save_word2vec_format("my_w2v")
        wv.load_word2vec_format("")
        
        # Getting champion list
        champion_names : list[str] = list()
        with open("./datasets/champion_mapping.json", "r") as file:
            champion_mapping : dict = json.load(file)
            champion_names = [s.lower() for s in list(champion_mapping.keys())]
        
        print("Most similar words for alistar : ")
        for w, sim in wv.most_similar("alistar"):
            print((w, sim))
        print("\n------\n")
        print("Most similar words for rell")
        for w, sim in wv.most_similar("rell"):
            print((w, sim))
        
        