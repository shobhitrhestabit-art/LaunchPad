from src.retriever.retrieval_types import RetrievalMode

def infer_mode_from_endpoint(endpoint: str)-> RetrievalMode:
    endpoint = endpoint.lower()
    if "image" in endpoint:
        return RetrievalMode.IMAGE
    elif "sql" in endpoint:
        return RetrievalMode.SQL
    else:
        return RetrievalMode.TEXT