from src.embeddings.embedder import model
from src.vectorstore.qdrant_store import get_qdrant_client, COLLECTION_NAME


def retrieve(query: str, k: int = 5):
    """
    Retrieve top-k relevant chunks from Qdrant for a user query
    """

   
    query_vector = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    
    client = get_qdrant_client()

    
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=k,
        with_payload=True
    )

    return response.points


def run_query_engine():
    print(" Qdrant Query Engine")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Enter your query: ").strip()

        if query.lower() in {"exit", "quit"}:
            print(" Exiting query engine")
            break

        if not query:
            print(" Empty query. Try again.\n")
            continue

        results = retrieve(query, k=5)

        if not results:
            print(" No relevant results found.\n")
            continue

        print("\n Retrieved Results:\n")

        for i, hit in enumerate(results, start=1):
            payload = hit.payload

            print(f"--- Result {i} ---")
            print(f"Score : {hit.score:.4f}")
            print(f"Source: {payload.get('source')}")
            print(f"Page  : {payload.get('page_number')}")
            print(f"Text  : {payload.get('text', '')[:300]}...")
            print()

        print("=" * 60)


if __name__ == "__main__":
    run_query_engine()
