import json 
from pathlib import Path
import re
from typing import List

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter




BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw" / "rawpdfs"
CHUNKS_DIR = BASE_DIR / "data" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS_FILE = CHUNKS_DIR / "chunks.jsonl"



def clean_text(text: str) -> str:
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()



def load_documents() -> List[Document]:
    documents: List[Document] = []

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    for file in DATA_DIR.iterdir():
        try:
            if file.suffix == ".pdf":
                loader = PyPDFLoader(str(file))
                docs = loader.load()

                for d in docs:
                    d.page_content = clean_text(d.page_content)
                    d.metadata.update({
                        "source": file.name,
                        "page_number": d.metadata.get("page"),
                        "tags": ["pdf"],
                    })
                    documents.append(d)

            elif file.suffix == ".txt":
                loader = TextLoader(str(file))
                docs = loader.load()

                for d in docs:
                    d.page_content = clean_text(d.page_content)
                    d.metadata.update({
                        "source": file.name,
                        "page_number": None,
                        "tags": ["txt"],
                    })
                    documents.append(d)

            elif file.suffix == ".csv":
                loader = CSVLoader(str(file))
                docs = loader.load()

                for d in docs:
                    d.page_content = clean_text(d.page_content)
                    d.metadata.update({
                        "source": file.name,
                        "page_number": d.metadata.get("row"),
                        "tags": ["csv"],
                    })
                    documents.append(d)

        except DependencyError:
            print(f" Skipping encrypted PDF: {file.name}")

        except PdfReadError:
            print(f"Corrupt PDF skipped: {file.name}")

        except Exception as e:
            print(f" Failed to load {file.name}: {e}")

    return documents

def chunk_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk_{i}"

    return chunks

def save_chunks(chunks: List[Document]):
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            record = {
                "text": chunk.page_content,
                "metadata": chunk.metadata
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"💾 Saved {len(chunks)} chunks to {CHUNKS_FILE}")


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    save_chunks(chunks)

    print("Documents loaded:", len(docs))
    print("Chunks created:", len(chunks))
