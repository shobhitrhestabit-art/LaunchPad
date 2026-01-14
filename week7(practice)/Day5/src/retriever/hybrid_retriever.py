from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.retriever.qdrant_retriever import QdrantRetriever
from src.retriever.retrieval_types import RetrievalMode


class HybridRetriever:
    def __init__(self, top_k: int = 5):
        self.base_retriever = QdrantRetriever(top_k=top_k)

    def retrieve(self, query: str, mode: RetrievalMode):
        if not query or not query.strip():
            return []

        query_filter = self._build_filter(mode)

        return self.base_retriever.search(
            query=query,
            query_filter=query_filter
        )

    def _build_filter(self, mode: RetrievalMode):
        if mode == RetrievalMode.TEXT:
            return Filter(
                must=[
                    FieldCondition(
                        key="source_type",
                        match=MatchValue(value="text")
                    )
                ]
            )

        if mode == RetrievalMode.IMAGE:
            return Filter(
                must=[
                    FieldCondition(
                        key="source_type",
                        match=MatchValue(value="image")
                    )
                ]
            )

        if mode == RetrievalMode.SQL:
            return Filter(
                must=[
                    FieldCondition(
                        key="source_type",
                        match=MatchValue(value="sql")
                    )
                ]
            )

        return None
