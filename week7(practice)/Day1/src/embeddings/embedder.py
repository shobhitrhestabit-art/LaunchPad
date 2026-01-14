from sentence_transformers import SentenceTransformer

#embedding model 
model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_chunks(chunks):
    """
    Converts document chunks into embeddings
    """
    if not chunks:
        raise ValueError("No chunks provided for embedding")

    texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings
