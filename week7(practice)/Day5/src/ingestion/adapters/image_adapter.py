from pathlib import Path
from PIL import Image
import pytesseract

from src.ingestion.models import IngestDocument


def load_image(image_path: str) -> IngestDocument:
    """
    Runs OCR on an image and returns text as IngestDocument.
    """
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image)

    return IngestDocument(
        text=ocr_text,
        source_type="image",
        source_id=Path(image_path).name,
        metadata={
            "ocr_engine": "tesseract"
        }
    )
