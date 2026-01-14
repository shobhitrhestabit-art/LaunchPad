from typing import Dict
from src.embeddings.embedding_service import embed_texts
from src.llm.answer_generator import generate_answer
import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def context_match_score(answer: str, context: str) -> float:
    """
    Measures how semantically grounded the answer is in the context
    """
    answer_emb = embed_texts([answer])[0]
    context_emb = embed_texts([context])[0]

    score = cosine_similarity(answer_emb, context_emb)
    return round(float(score), 3)


def self_critique(query: str, context: str, answer: str) -> Dict:
    """
    LLM evaluates its own answer
    """

    critique_prompt = f"""
You are reviewing an AI-generated answer.

QUESTION:
{query}

CONTEXT:
{context}

ANSWER:
{answer}

TASK:
- Check if the answer is fully supported by the context.
- Identify any unsupported or speculative claims.
- Respond in JSON.

FORMAT:
{{
  "needs_refinement": true | false,
  "reason": "short explanation"
}}
""".strip()

    critique = generate_answer("Self critique", critique_prompt)

    # Fallback if model responds badly
    try:
        import json
        return json.loads(critique)
    except Exception:
        return {
            "needs_refinement": True,
            "reason": "Critique parsing failed"
        }


def evaluate_answer(query: str, context: str, answer: str) -> Dict:
    """
    Combines all evaluation signals
    """

    ctx_score = context_match_score(answer, context)
    critique = self_critique(query, context, answer)

    # Faithfulness logic
    if ctx_score >= 0.5 and critique["needs_refinement"] is False:
        verdict = "accept"
        confidence = "high"

    elif ctx_score >= 0.4:
        verdict = "warn"
        confidence = "medium"

    else:
        verdict = "reject"
        confidence = "low"

    return {
        "context_match_score": ctx_score,
        "self_critique": critique,
        "verdict": verdict,
        "confidence": confidence
    }
