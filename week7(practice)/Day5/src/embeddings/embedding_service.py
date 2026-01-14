from sentence_transformers import SentenceTransformer

from src.config.settings import (
    EMBEDDING_MODEL,
    EMBEDDING_BATCH_SIZE,
    NORMALIZE_EMBEDDINGS
)

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_texts(texts):
    model = get_model()
    return model.encode(
        texts,
        batch_size=EMBEDDING_BATCH_SIZE,
        normalize_embeddings=NORMALIZE_EMBEDDINGS
    )


def get_embedding_dim():
    model = get_model()
    return model.get_sentence_embedding_dimension()
