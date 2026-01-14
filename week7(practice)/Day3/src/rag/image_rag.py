# src/rag/image_rag.py

from typing import Dict, List
from src.retriever.image_search import ImageRetriever


class ImageRAG:
    def __init__(self, top_k: int = 5):
        self.retriever = ImageRetriever(top_k=top_k)

    def explain_image(self, image_path: str) -> Dict:
        # 1️⃣ Retrieve similar images
        results = self.retriever.search_by_image(image_path)

        context_blocks: List[str] = []

        # 2️⃣ Collect OCR text
        for idx, res in enumerate(results, start=1):
            ocr_text = res.get("ocr_text", "").strip()
            caption = res.get("caption", "").strip()
            block = f"[Source {idx}]"
            if caption:
                block += f"\nCaption: {caption}"
            if ocr_text:
                block += f"\nOCR: {ocr_text}"

            context_blocks.append(block)

           
        # 3️⃣ Build explanation (NO LLM)
        explanation = (
            "Based on visually similar documents, the image appears to be related to:\n\n"
            + "\n\n".join(context_blocks)
        )

        return {
            "image": image_path,
            "explanation": explanation,
            "sources_used": len(context_blocks),
        }
