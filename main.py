from services.create_database import create_mobalytics_database, create_youtube_database, create_wiki_database
from services.api.youtube.youtube_data import push_audio_dataset
from services.utils import regenerate_error_lines
from services.data_augmentation.augment_data import augment_data

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-db-mobalytics", action="store_true", default=False, help="Create database from mobalytics")
    parser.add_argument("--create-db-youtube", action="store_true", default=False, help="Create database from youtube")
    parser.add_argument("--create-db-wiki", action="store_true", default=False, help="Create database from the league of legends wiki")
    parser.add_argument("--push-db-youtube", action="store_true", default=False, help="Putsh to HF dataset from youtube")
    parser.add_argument("--db-type", metavar="[str]", type=str, help="Tells wich type of database you want to create")
    parser.add_argument("--db-name", metavar="[str]", type=str, help="Name of database")
    parser.add_argument("--load-word-embedding", metavar="[uuid]", type=str, help="Load a give w2v model")
    parser.add_argument("--data-augmentation", action="store_true", default=False, help="Create a new dataset with data augmentation")
    args = parser.parse_args()
    args_data = vars(args)
       
    if args_data["create_db_mobalytics"]:
        db_name : str = args_data["db_name"]
        db_type : str = args_data["db_type"]
        assert db_type != None
        assert db_name != None
        create_mobalytics_database(db_name, db_type)
        
    elif args_data["create_db_youtube"]:
        # push_audio_dataset()
        create_youtube_database()
        regenerate_error_lines()
    
    elif args_data["create_db_wiki"]:
        create_wiki_database(["champions"], False)
    
    elif args_data["push_db_youtube"]:
        push_audio_dataset()
        
    elif args_data["data_augmentation"]:
        augment_data("./data/fill-mask/v6/", "./error_ids_mu.json", "mu")
        
    