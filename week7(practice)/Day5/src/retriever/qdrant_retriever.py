from qdrant_client.models import Filter
from src.embeddings.embedding_service import embed_texts
from src.embeddings.embed_and_store import get_client
from src.config.settings import QDRANT_COLLECTION


class QdrantRetriever:
    def __init__(self, top_k: int = 5):
        self.client = get_client()
        self.top_k = top_k

    def search(self, query: str, query_filter: Filter | None = None):
        if not query or not query.strip():
            return []

        query_vector = embed_texts([query])[0]

        results = self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            query_filter=query_filter,
            limit=self.top_k,
            with_payload=True
        ).points

        chunks = []
        for r in results:
            payload = r.payload or {}
            payload["score"] = r.score
            chunks.append(payload)

        return chunks
