from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader
import json
from sklearn.cluster import KMeans

from packages.models.sentence_transformer.sentence_transformer import prepare_dataset, prepare_model, train_model, getSimilarity
from packages.utils.utils_func import get_token
def create_word_embedding():
    model : SentenceTransformer = prepare_model()
    dataset : DataLoader = prepare_dataset()
    train_model(model, dataset)

def getWordSimilarity(word1 : str, word2 : str):
    getSimilarity(word1, word2)


def clusteringChamps():
    with open("./datasets/champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)
        champion_names : list[str] = list(champion_mapping.keys())
        champion_names = [s.lower() for s in champion_names]
        corpus = champion_names
        token = get_token("read")
        embedder = SentenceTransformer("avinot/distilroberta-base-LoL-Champions", token=token)

        corpus_embeddings = embedder.encode(corpus)


        num_clusters = 6
        clustering_model = KMeans(n_clusters=num_clusters)
        clustering_model.fit(corpus_embeddings)
        cluster_assignment = clustering_model.labels_

        clustered_sentences = [[] for i in range(num_clusters)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            clustered_sentences[cluster_id].append(corpus[sentence_id])

        for i, cluster in enumerate(clustered_sentences):
            print("Cluster ", i + 1)
            print(cluster)
            print("")