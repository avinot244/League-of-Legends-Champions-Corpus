from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader
from gensim.models.word2vec import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

from packages.models.sentence_transformer import prepare_dataset_bert, prepare_model_bert, train_model_bert
from packages.models.w2v.word2vec import prepare_dataset_w2v, train_model_w2v
def create_bert_word_embedding():
    model : SentenceTransformer = prepare_model_bert()
    dataset : DataLoader = prepare_dataset_bert()
    train_model_bert(model, dataset)

def create_word2vec_word_embedding():
    model : Word2Vec = Word2Vec(vector_size=100, min_count=1)
    print("Preparing dataset")
    dataset : list = prepare_dataset_w2v()
    print("Training model")
    (model, vocab) = train_model_w2v(model, dataset)
    # word_embeddings = np.array([ model.wv[k] if k in model.wv else np.zeros(100) for k in vocab ])
    return vocab, model.wv
    