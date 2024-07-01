from datasets import load_dataset
from sentence_transformers import InputExample, SentenceTransformer, models, losses
from torch.utils.data import DataLoader
from packages.utils.utils_func import get_token
import torch

def prepare_model() -> SentenceTransformer:
    print(f"{' Setting up the model ' :#^50}")
    word_embedding_model = models.Transformer("distilroberta-base")
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    return model

def prepare_dataset() -> DataLoader:
    print(f"{' Setting up the dataset ' :#^50}")
    # Loading dataset
    dataset_id = "avinot/LoL-Champions-semantic-classification"
    dataset = load_dataset(dataset_id)

    # Convert traning examples
    train_examples = []
    train_data = dataset['train']['set']
    n_examples = dataset['train'].num_rows
    for i in range(n_examples):
        example = train_data[i]
        train_examples.append(InputExample(texts=[example[0], example[1]]))
    
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    return train_dataloader

def train_model(model : SentenceTransformer, train_dataloader : DataLoader):
    print(f"{' training the model ' :#^50}")
    train_loss  = losses.MultipleNegativesRankingLoss(model=model)
    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10)
    write_token = get_token("write")
    model.push_to_hub(
        "distilroberta-base-LoL-Champions",
        token=write_token,
        train_datasets=["avinot/LoL-Champions-semantic-classification"]
    )

def getSimilarity(word1 : str, word2 : str) -> torch.Tensor:
    model = SentenceTransformer("avinot/distilroberta-base-LoL-Champions")
    embedding1 = model.encode(word1)
    embedding2 = model.encode(word2)
    similarity = model.similarity(embedding1, embedding2)
    print("Similarity of {} and {} : {}".format(word1, word2, similarity))
    print(type(similarity))
    return similarity
    
