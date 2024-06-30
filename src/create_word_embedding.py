from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader

from packages.models.sentence_transformer.sentence_transformer import prepare_dataset, prepare_model, train_model

def create_word_embedding():
    model : SentenceTransformer = prepare_model()
    dataset : DataLoader = prepare_dataset()
    train_model(model, dataset)