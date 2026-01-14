from fastapi import FastAPI
import uuid

from src.retriever import HybridRetriever, RetrievalMode
from src.pipelines.context_builder import build_context
from src.llm.answer_generator import generate_answer
from src.evaluation.rag_eval import evaluate_answer
from src.deployment.schemas import AskRequest
from src.memory.memory_store import MemoryStore

app = FastAPI(title="Day-5 RAG API")

retriever = HybridRetriever(top_k=5)

MAX_RETRIES = 2


def handle_query(query: str, mode: RetrievalMode):
    session_id = str(uuid.uuid4())
    memory = MemoryStore(session_id)

    
    chunks = retriever.retrieve(query, mode)

    if not chunks:
        return {
            "answer": "No relevant information found in the knowledge base.",
            "retrieved_context": "",
            "sources": [],
            "evaluation": {
                "verdict": "reject",
                "confidence": "low",
                "context_match_score": 0.0,
                "self_critique": {
                    "needs_refinement": True,
                    "reason": "No relevant context retrieved"
                }
            },
            "session_id": session_id
        }

    
    context, sources = build_context(chunks)

    if not context.strip():
        return {
            "answer": "Retrieved documents did not contain usable information.",
            "retrieved_context": "",
            "sources": sources,
            "evaluation": {
                "verdict": "reject",
                "confidence": "low",
                "context_match_score": 0.0,
                "self_critique": {
                    "needs_refinement": True,
                    "reason": "Empty context after processing"
                }
            },
            "session_id": session_id
        }

    
    attempt = 0
    final_answer = None
    final_evaluation = None

    while attempt < MAX_RETRIES:
        strict = attempt > 0

        answer = generate_answer(
            query=query,
            context=context,
            strict=strict
        )

        evaluation = evaluate_answer(query, context, answer)

        if evaluation["verdict"] in ("accept", "warn"):
            final_answer = answer
            final_evaluation = evaluation
            break

        attempt += 1


    if final_answer is None:
        final_answer = (
            "I don’t have enough reliable information in the provided documents "
            "to answer this question confidently."
        )
        final_evaluation = {
            "verdict": "reject",
            "confidence": "low",
            "context_match_score": 0.0,
            "self_critique": {
                "needs_refinement": True,
                "reason": "Answer could not be grounded in context"
            }
        }

   
    if final_evaluation["verdict"] in ("accept", "warn"):
        memory.add_message("user", query)
        memory.add_message("assistant", final_answer)

    memory.log_interaction({
        "query": query,
        "mode": mode.value,
        "answer": final_answer,
        "evaluation": final_evaluation,
        "sources": sources
    })

    
    return {
        "answer": final_answer,
        "retrieved_context": context,
        "sources": sources,
        "evaluation": final_evaluation,
        "session_id": session_id
    }


@app.post("/ask")
def ask(req: AskRequest):
    return handle_query(req.query, RetrievalMode.TEXT)


@app.post("/ask-image")
def ask_image(req: AskRequest):
    return handle_query(req.query, RetrievalMode.IMAGE)


@app.post("/ask-sql")
def ask_sql(req: AskRequest):
    return handle_query(req.query, RetrievalMode.SQL)
