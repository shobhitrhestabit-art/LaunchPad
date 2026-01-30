import faiss
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

STORAGE_DIR = "memory/storage"
INDEX_PATH = os.path.join(STORAGE_DIR, "faiss.index")
DOCS_PATH = os.path.join(STORAGE_DIR, "documents.pkl")
META_PATH = os.path.join(STORAGE_DIR, "metadata.pkl")

# Thread pool for blocking operations
_executor = ThreadPoolExecutor(max_workers=2)


class VectorMemory:
    def __init__(self, dim: int = 384, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize Vector Memory with FAISS and Sentence Transformers.
        
        Args:
            dim: Embedding dimension (384 for all-MiniLM-L6-v2)
            model_name: SentenceTransformer model to use
        """
        os.makedirs(STORAGE_DIR, exist_ok=True)

        self.dim = dim
        self.model_name = model_name
        
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}: {e}")

        # Load or create FAISS index
        if os.path.exists(INDEX_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)
            except Exception as e:
                print(f" Failed to load FAISS index, creating new one: {e}")
                self.index = faiss.IndexFlatL2(dim)
        else:
            self.index = faiss.IndexFlatL2(dim)

        # Load or create document store
        if os.path.exists(DOCS_PATH):
            try:
                with open(DOCS_PATH, "rb") as f:
                    self.store = pickle.load(f)
            except Exception as e:
                print(f" Failed to load documents, creating new store: {e}")
                self.store = []
        else:
            self.store = []

        # Load metadata (timestamps, sources, etc.)
        if os.path.exists(META_PATH):
            try:
                with open(META_PATH, "rb") as f:
                    self.metadata = pickle.load(f)
            except Exception as e:
                print(f" Failed to load metadata, creating new: {e}")
                self.metadata = []
        else:
            self.metadata = []

    def embed(self, text: str) -> np.ndarray:
        """
        Embed text using the model.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as float32 numpy array
        """
        try:
            if not text or not isinstance(text, str):
                return np.zeros(self.dim, dtype="float32")
            
            # Clean text
            text = text.strip()
            if not text:
                return np.zeros(self.dim, dtype="float32")
            
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.astype("float32")
        except Exception as e:
            print(f" Embedding failed: {e}")
            return np.zeros(self.dim, dtype="float32")

    def add(self, text: str, metadata: Optional[dict] = None) -> bool:
        """
        Add text to memory with optional metadata.
        
        Args:
            text: Text to store
            metadata: Optional metadata dict (source, timestamp, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text or not isinstance(text, str):
                return False
            
            text = text.strip()
            if not text or len(text) < 3:  # Skip very short texts
                return False

            # Avoid duplicates
            if text in self.store:
                return False

            # Embed and add to index
            vector = np.array([self.embed(text)]).astype("float32")
            self.index.add(vector)
            self.store.append(text)
            
            # Store metadata
            if metadata is None:
                metadata = {}
            self.metadata.append(metadata)

            # Persist immediately
            self._save()
            return True
        except Exception as e:
            print(f" Error adding to memory: {e}")
            return False

    def search(self, query: str, k: int = 3) -> List[str]:
        """
        Search for similar documents.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of matching documents
        """
        try:
            if self.index.ntotal == 0:
                return []

            if not query or not isinstance(query, str):
                return []

            # Limit k to actual store size
            k = min(k, len(self.store))
            if k <= 0:
                return []

            query_vec = np.array([self.embed(query)]).astype("float32")
            distances, indices = self.index.search(query_vec, k)

            # Filter valid results
            results = []
            for i, idx in enumerate(indices[0]):
                if 0 <= idx < len(self.store):
                    results.append({
                        "text": self.store[idx],
                        "distance": float(distances[0][i]),
                        "metadata": self.metadata[idx] if idx < len(self.metadata) else {}
                    })
            
            return results
        except Exception as e:
            print(f" Search failed: {e}")
            return []

    def search_texts(self, query: str, k: int = 3) -> List[str]:
        """
        Search and return only text results (for backward compatibility).
        
        Args:
            query: Query string
            k: Number of results
            
        Returns:
            List of matching text strings
        """
        results = self.search(query, k)
        return [r["text"] for r in results]

    def clear(self) -> bool:
        """Clear all memory."""
        try:
            self.index = faiss.IndexFlatL2(self.dim)
            self.store = []
            self.metadata = []
            self._save()
            return True
        except Exception as e:
            print(f" Error clearing memory: {e}")
            return False

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "total_documents": len(self.store),
            "index_size": self.index.ntotal,
            "model": self.model_name,
            "embedding_dim": self.dim,
            "storage_path": STORAGE_DIR
        }

    async def add_async(self, text: str, metadata: Optional[dict] = None) -> bool:
        """
        Async wrapper for adding to memory.
        
        Args:
            text: Text to store
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _executor,
            self.add,
            text,
            metadata
        )

    async def search_async(self, query: str, k: int = 3) -> List[str]:
        """
        Async wrapper for searching.
        
        Args:
            query: Query string
            k: Number of results
            
        Returns:
            List of matching text strings
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            _executor,
            self.search_texts,
            query,
            k
        )
        return results

    def _save(self) -> None:
        """Persist memory to disk."""
        try:
            faiss.write_index(self.index, INDEX_PATH)
            with open(DOCS_PATH, "wb") as f:
                pickle.dump(self.store, f)
            with open(META_PATH, "wb") as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            print(f" Failed to save memory: {e}")

    def __len__(self) -> int:
        """Return number of documents in memory."""
        return len(self.store)

    def __repr__(self) -> str:
        return f"VectorMemory(docs={len(self.store)}, model={self.model_name})"