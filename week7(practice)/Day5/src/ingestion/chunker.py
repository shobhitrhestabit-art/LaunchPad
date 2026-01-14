

def chunk_document(doc, chunk_size,overlap):
    text = doc.text
    chunks = []
    start  =0
    chunk_id =0


    while start < len(text):
        end = start + chunk_size
        chunk_tetx = text[start:end]

        chunks.append(
            {
                "text": chunk_tetx,
                "source_type": doc.source_type,
                "source_id": doc.source_id,
                "chunk_id": chunk_id

            }
        )
        start = end - overlap
        chunk_id += 1

    return chunks