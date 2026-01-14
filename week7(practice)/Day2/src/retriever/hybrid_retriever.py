import re
from qdrant_client import models  # Added this import
from src.embeddings.embedder import model
from src.vectorstore.qdrant_store import get_qdrant_client, COLLECTION_NAME


def keyword_score(query: str, text: str) -> int:
    words = re.findall(r"\w+", query.lower())
    text = text.lower()
    return sum(1 for w in words if w in text)


class HybridRetriever:
    def __init__(self, candidate_k: int = 20):
        self.client = get_qdrant_client()
        self.candidate_k = candidate_k

    def retrieve(self, query: str, filters: dict | None = None):
        # Generate query vector
        query_vector = model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        # FIX: Changed 'filter' to 'query_filter'
        response = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=self.candidate_k,
            with_payload=True,
            query_filter=self._build_filter(filters) 
        )

        candidates = []
        for hit in response.points:
            candidates.append({
                "text": hit.payload["text"],
                "metadata": hit.payload,
                "vector_score": hit.score,
                "keyword_score": keyword_score(query, hit.payload["text"])
            })

        return candidates

    def _build_filter(self, filters):
        if not filters:
            return None

        # FIX: Use the Qdrant models.Filter for proper structure
        return models.Filter(
            must=[
                models.FieldCondition(
                    key=k, 
                    match=models.MatchValue(value=v)
                )
                for k, v in filters.items()
            ]
        )