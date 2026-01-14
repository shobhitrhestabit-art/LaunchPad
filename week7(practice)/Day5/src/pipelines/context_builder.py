from typing import List, Dict, Tuple


def build_context(
    chunks: List[Dict],
    max_chars: int = 4000
) -> Tuple[str, List[Dict]]:
    """
    Build a clean context string and source list from retrieved chunks.

    Returns:
        context (str)
        sources (list of dict)
    """

    if not chunks:
        return "", []

   
    chunks = sorted(chunks, key=lambda x: x.get("score", 0), reverse=True)

    seen = set()
    context_parts = []
    sources = []
    total_chars = 0

   
    for chunk in chunks:
        unique_key = (
            chunk.get("source_type"),
            chunk.get("source_id"),
            chunk.get("chunk_id")
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        text = chunk.get("text", "").strip()
        if not text:
            continue

        
        if total_chars + len(text) > max_chars:
            break

        context_parts.append(text)
        total_chars += len(text)

        sources.append({
            "source_type": chunk.get("source_type"),
            "source_id": chunk.get("source_id"),
            "score": round(chunk.get("score", 0), 3)
        })

   
    context = "\n\n---\n\n".join(context_parts)

    return context, sources
