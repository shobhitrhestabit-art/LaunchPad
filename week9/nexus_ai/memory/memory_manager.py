from memory.vector_memory import VectorMemory
from typing import List, Optional, Dict
import asyncio


class MemoryManager:
    """
    High-level memory management interface for the orchestrator.
    Handles long-term storage and retrieval of task results and context.
    """
    
    def __init__(self):
        """Initialize the memory manager with vector memory backend."""
        try:
            self.vector_memory = VectorMemory()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MemoryManager: {e}")

    def add_long_term(self, text: str, metadata: Optional[Dict] = None) -> bool:
        """
        Store text in long-term memory with optional metadata.
        
        Args:
            text: Content to store (typically agent output)
            metadata: Optional metadata (source, timestamp, type, etc.)
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> mm = MemoryManager()
            >>> mm.add_long_term(
            ...     "Research findings about AI",
            ...     metadata={"agent": "Researcher", "timestamp": "2024-01-01"}
            ... )
            True
        """
        if not text:
            return False
        
        try:
            return self.vector_memory.add(text, metadata)
        except Exception as e:
            print(f" Error in add_long_term: {e}")
            return False

    def recall(self, query: str, k: int = 3) -> List[str]:
        """
        Retrieve relevant memories based on semantic similarity.
        
        Args:
            query: Query string to search for
            k: Number of results to return (default: 3)
            
        Returns:
            List of relevant text snippets from memory
            
        Example:
            >>> mm = MemoryManager()
            >>> results = mm.recall("machine learning research", k=5)
            >>> for result in results:
            ...     print(result)
        """
        if not query:
            return []
        
        try:
            return self.vector_memory.search_texts(query, k)
        except Exception as e:
            print(f" Error in recall: {e}")
            return []

    def recall_with_metadata(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieve memories with full metadata.
        
        Args:
            query: Query string
            k: Number of results
            
        Returns:
            List of dicts with 'text', 'distance', and 'metadata'
            
        Example:
            >>> results = mm.recall_with_metadata("AI safety")
            >>> for result in results:
            ...     print(f"Text: {result['text']}")
            ...     print(f"Score: {result['distance']}")
            ...     print(f"Source: {result['metadata'].get('agent')}")
        """
        if not query:
            return []
        
        try:
            return self.vector_memory.search(query, k)
        except Exception as e:
            print(f" Error in recall_with_metadata: {e}")
            return []

    async def add_long_term_async(self, text: str, metadata: Optional[Dict] = None) -> bool:
        """
        Async version of add_long_term for non-blocking storage.
        
        Args:
            text: Content to store
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        if not text:
            return False
        
        try:
            return await self.vector_memory.add_async(text, metadata)
        except Exception as e:
            print(f" Error in add_long_term_async: {e}")
            return False

    async def recall_async(self, query: str, k: int = 3) -> List[str]:
        """
        Async version of recall for non-blocking retrieval.
        
        Args:
            query: Query string
            k: Number of results
            
        Returns:
            List of relevant memories
        """
        if not query:
            return []
        
        try:
            return await self.vector_memory.search_async(query, k)
        except Exception as e:
            print(f" Error in recall_async: {e}")
            return []

    def clear(self) -> bool:
        """
        Clear all memories. Use with caution!
        
        Returns:
            True if successful
        """
        try:
            return self.vector_memory.clear()
        except Exception as e:
            print(f" Error clearing memory: {e}")
            return False

    def get_stats(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory stats
            
        Example:
            >>> stats = mm.get_stats()
            >>> print(f"Total documents: {stats['total_documents']}")
        """
        try:
            return self.vector_memory.get_stats()
        except Exception as e:
            print(f" Error getting stats: {e}")
            return {}

    def __len__(self) -> int:
        """Return number of memories stored."""
        return len(self.vector_memory)

    def __repr__(self) -> str:
        stats = self.get_stats()
        return f"MemoryManager(docs={stats.get('total_documents', 0)})"


# Convenience function for quick access
def get_memory_manager() -> MemoryManager:
    """
    Get a singleton-like MemoryManager instance.
    
    Returns:
        MemoryManager instance
    """
    return MemoryManager()