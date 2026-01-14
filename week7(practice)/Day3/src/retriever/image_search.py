from pathlib import Path
from typing import List, Dict
from PIL import Image

from src.embeddings.query_embedder import QueryEmbedder
from src.vectorstore.multimodal_index import MultimodalVectorStore


class ImageRetriever:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.embedder = QueryEmbedder()
        self.store = MultimodalVectorStore()
        base_dir = Path(__file__).resolve().parents[2]
        self.image_dir = base_dir / "src" / "storage" / "images"

    def search_by_text(self, query: str) -> List[Dict]:
        query_vector = self.embedder.embed_text_query(query)

        response = self.store.client.query_points(
            collection_name=self.store.collection_name,
            query=query_vector,
            using="text",
            limit=self.top_k,
            with_payload=True,
        )

        results = []
        for res in response.points:
            payload = res.payload or {}
            image_file = payload.get("image_file", "unknown.jpg")

            results.append(
                {
                    "score": res.score,
                    "image_path": str(self.image_dir / image_file),
                    "ocr_text": payload.get("ocr_text", ""),
                }
            )

        return results

    def search_by_image(self, image_path: str) -> List[Dict]:
        image = Image.open(image_path).convert("RGB")
        query_vector = self.embedder.embed_image_query(image)

        response = self.store.client.query_points(
            collection_name=self.store.collection_name,
            query=query_vector,
            using="image",
            limit=self.top_k,
            with_payload=True,
        )

        results = []
        for res in response.points:
            payload = res.payload or {}
            image_file = payload.get("image_file", "unknown.jpg")

            results.append(
                {
                    "score": res.score,
                    "image_path": str(self.image_dir / image_file),
                    "ocr_text": payload.get("ocr_text", ""),
                }
            )

        return results


def main():
    retriever = ImageRetriever(top_k=5)

    query = input("Enter text query: ").strip()
    if not query:
        print("Empty query")
        return

    results = retriever.search_by_text(query)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
