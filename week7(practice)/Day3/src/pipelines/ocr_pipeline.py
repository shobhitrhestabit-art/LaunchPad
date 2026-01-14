"""
OCR Pipeline (Day 3 – Image RAG)

Reads normalized images from src/storage/images
Extracts OCR text using Tesseract
Stores OCR output as JSON files in src/storage/ocr

Safe to re-run:
- Skips images that already have OCR JSON
"""

from pathlib import Path
import json
import logging
from datetime import datetime

from src.utils.ocr_utils import extract_text_from_image


# -------------------------------------------------
# PATH CONFIGURATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]  # Day3/

IMAGE_DIR = BASE_DIR / "src" / "storage" / "images"
OCR_OUTPUT_DIR = BASE_DIR / "src" / "storage" / "ocr"

OCR_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# LOGGER
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def save_ocr_output(image_path: Path, text: str) -> None:
    """
    Save OCR output as a JSON file for one image.
    """
    output_file = OCR_OUTPUT_DIR / f"{image_path.stem}.json"

    data = {
        "image_file": image_path.name,
        "ocr_text": text,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

def run_ocr() -> None:
    if not IMAGE_DIR.exists():
        logger.error(f"Image directory not found: {IMAGE_DIR}")
        return

    logger.info(f"Starting OCR pipeline on images in: {IMAGE_DIR}")

    for image_path in sorted(IMAGE_DIR.glob("*.jpg")):
        output_json = OCR_OUTPUT_DIR / f"{image_path.stem}.json"

        # ✅ Skip if OCR already exists
        if output_json.exists():
            logger.info(f"OCR already exists for {image_path.name}, skipping.")
            continue

        logger.info(f"Running OCR on {image_path.name}")

        text = extract_text_from_image(image_path)

        save_ocr_output(image_path, text)

        logger.info(f"OCR saved → {output_json.name}")
        logger.info(text[:300])  # preview first 300 characters
        logger.info("-" * 60)

    logger.info("OCR pipeline completed successfully.")


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    run_ocr()
