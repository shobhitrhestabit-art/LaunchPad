from pydantic import BaseModel
from typing import List, Dict, Any


class AskRequest(BaseModel):
    query: str


class SourceChunk(BaseModel):
    source_type: str
    source_id: str
    score: float


class EvaluationResult(BaseModel):
    verdict: str
    confidence: str
    context_match_score: float
    self_critique: Dict[str, Any]


class AskResponse(BaseModel):
    answer: str
    retrieved_context: str
    sources: List[SourceChunk]
    evaluation: EvaluationResult
    session_id: str
