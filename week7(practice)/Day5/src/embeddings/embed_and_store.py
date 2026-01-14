import uuid
from hashlib import sha256

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from src.config.settings import (
    QDRANT_PATH,
    QDRANT_COLLECTION
)


def make_id(source_id, chunk_id, text):
    hash_hex = sha256(
        f"{source_id}_{chunk_id}_{text}".encode("utf-8")
    ).hexdigest()
    return str(uuid.UUID(hash_hex[:32]))


def get_client():
    return QdrantClient(path=QDRANT_PATH)


def recreate_collection(client, vector_size):
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )


def upsert_chunks(client, chunks, embeddings):
    points = []

    for chunk, vector in zip(chunks, embeddings):
        point_id = make_id(
            chunk["source_id"],
            chunk["chunk_id"],
            chunk["text"]
        )

        points.append(
            PointStruct(
                id=point_id,      
                vector=vector,
                payload=chunk
            )
        )

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points
    )
