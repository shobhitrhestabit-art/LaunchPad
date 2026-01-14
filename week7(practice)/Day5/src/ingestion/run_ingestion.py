from pathlib import Path
from tqdm import tqdm

from src.config.settings import (
    RAW_TEXT_DIR,
    RAW_IMAGE_DIR,
    DB_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from src.embeddings.embedding_service import get_embedding_dim




from src.ingestion.adapters.pdf_adapter import load_pdf
from src.ingestion.adapters.image_adapter import load_image
from src.ingestion.adapters.sql_adapter import load_sql_schema
from src.ingestion.chunker import chunk_document

from src.embeddings.embedding_service import embed_texts
from src.embeddings.embed_and_store import (
    get_client,
    recreate_collection,
    upsert_chunks
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
BATCH_SIZE = 32   # 👈 RAM control


def run():
    print(" Starting ingestion")

    client = get_client()
    vector_size = get_embedding_dim()
    recreate_collection(client,vector_size)

    # --------------------
    # 1. PDF ingestion
    # --------------------
    pdfs = list(Path(RAW_TEXT_DIR).glob("*.pdf"))

    for pdf in tqdm(pdfs, desc="PDF ingestion"):
        doc = load_pdf(str(pdf))
        _process_document(doc, client)

    # --------------------
    # 2. Image OCR
    # --------------------
    images = [
        img for img in Path(RAW_IMAGE_DIR).iterdir()
        if img.suffix.lower() in IMAGE_EXTENSIONS
    ]

    for img in tqdm(images, desc="Image OCR"):
        doc = load_image(str(img))
        if doc:
            _process_document(doc, client)

    # --------------------
    # 3. DB schema
    # --------------------
    tables = load_sql_schema(DB_PATH)

    for table_doc in tqdm(tables, desc="DB schema"):
        _process_document(table_doc, client)

    print(" Ingestion completed successfully")


def _process_document(doc, client):
    """
    Chunk → batch → embed → store
    """
    chunks = chunk_document(doc, CHUNK_SIZE, CHUNK_OVERLAP)

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]

        texts = [c["text"] for c in batch]
        embeddings = embed_texts(texts)

        upsert_chunks(client, batch, embeddings)


if __name__ == "__main__":
    run()
