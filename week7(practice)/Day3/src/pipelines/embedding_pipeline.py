from pathlib import Path
import uuid
import json
import logging

from src.embeddings.clip_embedder import CLIPEmbedder
from src.vectorstore.multimodal_index import MultimodalVectorStore


BASE_DIR = Path(__file__).resolve().parents[2]

IMAGE_DIR = BASE_DIR / "src" / "storage" / "images"
OCR_DIR = BASE_DIR / "src" / "storage" / "ocr"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_embedding_pipeline():
    embedder = CLIPEmbedder()
    store = MultimodalVectorStore()

    for image_path in sorted(IMAGE_DIR.glob("*.jpg")):
        ocr_path = OCR_DIR / f"{image_path.stem}.json"

        if not ocr_path.exists():
            logger.warning(f"OCR missing for {image_path.name}, skipping.")
            continue

        with open(ocr_path, "r", encoding="utf-8") as f:
            ocr_data = json.load(f)

        ocr_text = ocr_data.get("ocr_text", "")

        # ---- CREATE EMBEDDINGS ----
        image_vector = embedder.embed_image(image_path)
        text_vector = embedder.embed_text(ocr_text)

        # ---- STORE EMBEDDINGS ----
        store.upsert(
            point_id=str(uuid.uuid4()),
            image_vector=image_vector,
            text_vector=text_vector,
            payload={
                "image_file": image_path.name,
                "ocr_text": ocr_text,
                "source": "News",
            },
        )

        logger.info(f"Stored embeddings for {image_path.name}")

    logger.info("Embedding storage pipeline completed.")


if __name__ == "__main__":
    run_embedding_pipeline()
