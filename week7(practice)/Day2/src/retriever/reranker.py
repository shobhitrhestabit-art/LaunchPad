import numpy as np
from src.embeddings.embedder import model


class Reranker:
    def rerank(self, query: str, candidates: list, top_k: int = 5):
        query_vec = model.encode(
            query,
            normalize_embeddings=True
        )

        reranked = []
        for c in candidates:
            chunk_vec = model.encode(
                c["text"],
                normalize_embeddings=True
            )
            score = float(np.dot(query_vec, chunk_vec))
            reranked.append({**c, "rerank_score": score})

        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]
