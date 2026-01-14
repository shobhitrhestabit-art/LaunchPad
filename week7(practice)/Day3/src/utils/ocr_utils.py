"""
OCR Utilities (Day 3 – Image RAG)

This module contains reusable OCR logic.
Given a single image, it extracts text using Tesseract.

Used by:
- OCR pipeline
- Image → Text RAG
- Debugging / testing
"""

from pathlib import Path
import logging

from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)


def extract_text_from_image(image_path: Path) -> str:
    """
    Extract OCR text from a single image.

    Args:
        image_path (Path): Path to an image file

    Returns:
        str: Extracted text (empty string if OCR fails)
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        logger.error(f"Failed to open image {image_path.name}: {e}")
        return ""

    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed for {image_path.name}: {e}")
        return ""
