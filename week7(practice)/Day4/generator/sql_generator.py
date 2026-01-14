import requests
import os

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

def build_prompt(question, schema):
    return f"""
You are an expert SQL generator.

Schema:
{schema}

Rules:
- Generate only SELECT queries
- Use only the given tables and columns
- Do not explain anything
- Return only SQL

Question:
{question}
"""

def generate_sql(question, schema):
    prompt = build_prompt(question, schema)

    response = requests.post(
        f"{LLM_BASE_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "temperature": 0,
            "stream": False
        }
    )

    data = response.json()

    # Handle different Ollama response formats
    if "response" in data:
        return data["response"].strip()

    if "message" in data and "content" in data["message"]:
        return data["message"]["content"].strip()

    raise RuntimeError(f"Unexpected LLM response format: {data}")
