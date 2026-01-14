# ---------- DATA PATHS ----------
DATA_ROOT = "src/data"

RAW_TEXT_DIR = f"{DATA_ROOT}/raw/text"
RAW_IMAGE_DIR = f"{DATA_ROOT}/raw/images"
DB_PATH = f"{DATA_ROOT}/db/netflix.db"

# ---------- CHUNKING ----------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ---------- EMBEDDINGS ----------
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
EMBEDDING_BATCH_SIZE = 32
NORMALIZE_EMBEDDINGS = True

# ---------- QDRANT (LOCAL FILE MODE) ----------
QDRANT_PATH = "src/vectorstore/qdrant_data"
QDRANT_COLLECTION = "day5_rag"
