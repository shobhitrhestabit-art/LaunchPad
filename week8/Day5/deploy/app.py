# app.py

import uuid
import re
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from model_loader import load_model
from config import (
    HOST,
    PORT,
    SYSTEM_PROMPT,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
)


app = FastAPI(
    title="Local GGUF LLM API",
    description="Local LLM API using a quantised GGUF model (llama.cpp)",
    version="1.0.0"
)

# Load model once
llm = load_model()




class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="User input prompt")
    temperature: float = Field(
        DEFAULT_TEMPERATURE,
        ge=0.1,
        le=2.0,
        description="Controls randomness"
    )
    top_p: float = Field(
        DEFAULT_TOP_P,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling"
    )



class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_k: int = DEFAULT_TOP_K
    top_p: float = DEFAULT_TOP_P



def clean_output(text: str) -> str:
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def build_prompt(system_prompt: str, user_prompt: str) -> str:
    return f"""<|system|>
{system_prompt}
<|user|>
{user_prompt}
<|assistant|>
"""


def validate_prompt(prompt: str) -> bool:
    if len(prompt.strip()) < 5:
        return False
    if len([c for c in prompt if c.isalpha()]) < len(prompt) * 0.3:
        return False
    return True



@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}



@app.post("/generate")
def generate(req: GenerateRequest):
    if not validate_prompt(req.prompt):
        raise HTTPException(
            status_code=400,
            detail="Prompt is too short or invalid"
        )

    try:
        prompt = build_prompt(SYSTEM_PROMPT, req.prompt)

        output = llm(
            prompt,
            max_tokens=DEFAULT_MAX_TOKENS,   
            temperature=req.temperature,     
            top_k=DEFAULT_TOP_K,             
            top_p=req.top_p,                
            stop=["<|user|>", "<|system|>"],
            echo=False
        )

        text = clean_output(output["choices"][0]["text"])

        return {
            "request_id": str(uuid.uuid4()),
            "text": text,
            "tokens_used": output["usage"]["completion_tokens"],
            "model_info": {
                "temperature": req.temperature,
                "top_p": req.top_p,
                "max_tokens": DEFAULT_MAX_TOKENS,
                "top_k": DEFAULT_TOP_K
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"<|system|>\n{SYSTEM_PROMPT}\n"

    for msg in req.messages:
        prompt += f"<|{msg.role}|>\n{msg.content}\n"

    prompt += "<|assistant|>\n"

    output = llm(
        prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_k=req.top_k,
        top_p=req.top_p,
        stop=["<|user|>", "<|system|>"]
    )

    text = clean_output(output["choices"][0]["text"])

    return {
        "request_id": str(uuid.uuid4()),
        "text": text,
        "tokens_used": output["usage"]["completion_tokens"]
    }
