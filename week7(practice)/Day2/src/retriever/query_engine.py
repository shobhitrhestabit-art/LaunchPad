from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.pipelines.context_builder import deduplicate, build_context

def run():
    query = input("Enter your query: ")

    retriever = HybridRetriever()
    reranker = Reranker()

    candidates = retriever.retrieve(
        query,
        #filters={"year": "2024", "type": "policy"}
    )

    reranked = reranker.rerank(query, candidates)
    final_chunks = deduplicate(reranked)
    print("\n===== CHUNKS (DEBUG) =====\n")
    for i, c in enumerate(final_chunks, 1):
        print(f"--- Chunk {i} ---")
        print(c["text"][:300])  # first 300 chars
        print()

    context, sources = build_context(final_chunks)

    print("\n===== CONTEXT =====\n")
    print(context)

    print("\n===== SOURCES =====")
    for s in sources:
        print(s)


if __name__ == "__main__":
    run()
