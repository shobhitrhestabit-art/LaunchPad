"""
Image Ingestion Pipeline (Day 3 – Image RAG)

Responsibilities:
- Walk through raw data folders
- Detect file type (image / pdf)
- Convert everything into normalized images
- Store processed images in src/storage/images

NOT included yet:
- OCR
- CLIP embeddings
- Vector DB
"""

from pathlib import Path
from typing import List
import shutil
import logging

from PIL import Image

try:
    from pdf2image import convert_from_path
    PDF_SUPPORTED = True
except ImportError:
    PDF_SUPPORTED = False


# ---------- CONFIG ----------

BASE_DIR = Path(__file__).resolve().parents[2]  # Day3/

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
STORAGE_IMAGE_DIR = BASE_DIR / "src" / "storage" / "images"


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}


# ---------- LOGGER ----------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ---------- HELPERS ----------

def ensure_storage_dir():
    """Ensure storage directory exists."""
    STORAGE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def normalize_and_save_image(
    image: Image.Image,
    output_path: Path
) -> None:
    """
    Normalize image and save it.

    Normalization:
    - Convert to RGB
    - Basic size safety (optional)
    """
    image = image.convert("RGB")
    image.save(output_path, format="JPEG")


# ---------- FILE HANDLERS ----------

def process_image_file(file_path: Path) -> None:
    """
    Process JPG / PNG images.
    """
    logger.info(f"Processing image: {file_path.name}")

    try:
        image = Image.open(file_path)
    except Exception as e:
        logger.error(f"Failed to open image {file_path.name}: {e}")
        return

    output_name = f"{file_path.stem}.jpg"
    output_path = STORAGE_IMAGE_DIR / output_name

    normalize_and_save_image(image, output_path)


def process_pdf_file(file_path: Path) -> None:
    """
    Process scanned PDF files by converting each page to an image.
    """
    if not PDF_SUPPORTED:
        logger.warning(f"PDF support not installed. Skipping {file_path.name}")
        return

    logger.info(f"Processing PDF: {file_path.name}")

    try:
        pages = convert_from_path(file_path)
    except Exception as e:
        logger.error(f"Failed to convert PDF {file_path.name}: {e}")
        return

    for idx, page in enumerate(pages, start=1):
        output_name = f"{file_path.stem}_page_{idx}.jpg"
        output_path = STORAGE_IMAGE_DIR / output_name
        normalize_and_save_image(page, output_path)


# ---------- MAIN INGESTION LOGIC ----------

def ingest_raw_data() -> None:
    """
    Walk through RAW_DATA_DIR and ingest all supported files.
    """
    ensure_storage_dir()

    logger.info(f"Starting ingestion from: {RAW_DATA_DIR}")

    for path in RAW_DATA_DIR.rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix in SUPPORTED_IMAGE_EXTENSIONS:
            process_image_file(path)

        elif suffix in SUPPORTED_PDF_EXTENSIONS:
            process_pdf_file(path)

        else:
            logger.info(f"Skipping unsupported file: {path.name}")

    logger.info("Ingestion completed.")


# ---------- ENTRY POINT ----------

if __name__ == "__main__":
    ingest_raw_data()
