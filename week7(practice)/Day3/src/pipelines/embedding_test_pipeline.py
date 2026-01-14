"""
Embedding Test Pipeline (Day 3 – Image RAG)

This pipeline ONLY:
- Loads images
- Loads OCR JSON
- Generates CLIP embeddings
- Prints embedding dimensions

NO storage
NO vector DB
NO Docker
"""

from pathlib import Path
import json
import logging

from src.embeddings.clip_embedder import CLIPEmbedder


# -------------------------------------------------
# PATH CONFIG
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

IMAGE_DIR = BASE_DIR / "src" / "storage" / "images"
OCR_DIR = BASE_DIR / "src" / "storage" / "ocr"


# -------------------------------------------------
# LOGGER
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------------------------------
# PIPELINE
# -------------------------------------------------

def run_embedding_test():
    logger.info("Starting embedding test pipeline")

    embedder = CLIPEmbedder()

    for image_path in sorted(IMAGE_DIR.glob("*.jpg")):
        ocr_path = OCR_DIR / f"{image_path.stem}.json"

        if not ocr_path.exists():
            logger.warning(f"OCR JSON missing for {image_path.name}, skipping.")
            continue

        with open(ocr_path, "r", encoding="utf-8") as f:
            ocr_data = json.load(f)

        ocr_text = ocr_data.get("ocr_text", "")

        # Generate embeddings
        image_vector = embedder.embed_image(image_path)
        text_vector = embedder.embed_text(ocr_text)

        logger.info(
            f"{image_path.name} | "
            f"image_dim={len(image_vector)} | "
            f"text_dim={len(text_vector)}"
        )

    logger.info("Embedding test pipeline completed.")


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    run_embedding_test()
