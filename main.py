from src.create_database import create_mobalytics_dataset, create_youtube_dataset, regenerate_error_lines
from src.create_word_embedding import create_bert_word_embedding, create_word2vec_word_embedding
from packages.db_manager.youtube.youtube_data import push_audio_dataset

import json
import argparse
from gensim.models.keyedvectors import KeyedVectors
import uuid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-mobalytics", action="store_true", default=False, help="Create database from mobalytics")
    parser.add_argument("--create-db-youtube", action="store_true", default=False, help="Create database from youtube")
    parser.add_argument("--push-db-youtube", action="store_true", default=False, help="Putsh to HF dataset from youtube")
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
        # push_audio_dataset()
        create_youtube_dataset()
        regenerate_error_lines()
    
    elif args_data["push_db_youtube"]:
        push_audio_dataset()
    
    elif args_data["word_embedding"] == "BERT":
        create_bert_word_embedding()
        
        
    