def deduplicate(chunks: list):
    seen = set()
    unique = []

    for c in chunks:
        key = (c["metadata"].get("source"), c["text"][:200])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique


def build_context(chunks: list, max_chars: int = 3000):
    context_parts = []
    sources = []
    used = 0

    for c in chunks:
        text = c["text"]
        if used + len(text) > max_chars:
            break

        context_parts.append(text)
        sources.append({
            "source": c["metadata"].get("source"),
            "page": c["metadata"].get("page_number")
        })
        used += len(text)

    return "\n\n".join(context_parts), sources
