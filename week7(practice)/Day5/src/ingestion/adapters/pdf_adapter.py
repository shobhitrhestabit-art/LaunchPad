from pathlib import Path
import fitz  # PyMuPDF

from src.ingestion.models import IngestDocument


def load_pdf(pdf_path: str) -> IngestDocument:
    """
    Reads a PDF and extracts all text.
    Returns a single IngestDocument.
    """
    doc = fitz.open(pdf_path)

    pages = []
    for page in doc:
        pages.append(page.get_text())

    full_text = "\n".join(pages)

    return IngestDocument(
        text=full_text,
        source_type="text",
        source_id=Path(pdf_path).name,
        metadata={
            "format": "pdf",
            "pages": len(doc)
        }
    )
