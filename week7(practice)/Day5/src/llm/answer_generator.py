import requests
import os
import json
from typing import List, Dict, Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def generate_answer(
    query: str,
    context: str,
    memory_messages: Optional[List[Dict]] = None,
    strict: bool = False
) -> str:

    system_prompt = (
        "You are a helpful assistant.\n"
        "Answer the question strictly using the context below.\n"
        "If the context does not contain enough information, say so clearly.\n"
    )

    if strict:
        system_prompt += (
            "Be extremely strict.\n"
            "Do NOT guess or add external knowledge.\n"
        )

    conversation = ""
    if memory_messages:
        conversation = "CONVERSATION SO FAR:\n"
        for msg in memory_messages:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")
            conversation += f"{role}: {content}\n"

    prompt = f"""
{system_prompt}

{conversation}

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
""".strip()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "temperature": 0.2,
            "stream": True
        },
        stream=True,
        timeout=None
    )

    response.raise_for_status()

    answer_parts: list[str] = []

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        data = json.loads(line)

        if data.get("response"):
            answer_parts.append(data["response"])

        if data.get("done"):
            break

    return "".join(answer_parts).strip()
