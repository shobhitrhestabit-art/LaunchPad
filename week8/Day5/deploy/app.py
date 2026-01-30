# app.py - IMPROVED VERSION

import uuid
import re
from typing import List, Optional
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

# ==============================
# FastAPI App
# ==============================

app = FastAPI(
    title="Local GGUF LLM API",
    description="Local LLM API using a quantised GGUF model (llama.cpp)",
    version="1.0.0"
)

# Load GGUF model ONCE at startup
llm = load_model()


# ==============================
# Request Schemas
# ==============================

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="The input prompt")
    max_tokens: int = Field(DEFAULT_MAX_TOKENS, ge=50, le=2048, description="Maximum tokens to generate")
    temperature: float = Field(DEFAULT_TEMPERATURE, ge=0.1, le=2.0, description="Sampling temperature")
    top_k: int = Field(DEFAULT_TOP_K, ge=1, le=100, description="Top-K sampling")
    top_p: float = Field(DEFAULT_TOP_P, ge=0.0, le=1.0, description="Top-P (nucleus) sampling")
    include_prompt: bool = Field(False, description="Include original prompt in response")
    context: Optional[str] = Field(None, description="Optional context/background information")


class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_k: int = DEFAULT_TOP_K
    top_p: float = DEFAULT_TOP_P


# ==============================
# Helper Functions
# ==============================

def clean_output(text: str) -> str:
    """
    Clean generated text by removing common artifacts and formatting issues.
    """
    # Remove markdown-style code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove incomplete sentences at the end
    if text and not text[-1] in '.!?':
        # Find last sentence ending
        last_period = max(
            text.rfind('.'),
            text.rfind('!'),
            text.rfind('?')
        )
        if last_period > len(text) * 0.3:  # Only if it's not too early
            text = text[:last_period + 1]
    
    # Remove common LLM artifacts
    unwanted_patterns = [
        r'\n\n+',  # Multiple newlines
        r'<\|.*?\|>',  # Chat tokens
        r'\[.*?\]',  # Bracket artifacts
        r'\*\*.*?\*\*',  # Bold markdown
    ]
    
    for pattern in unwanted_patterns:
        text = re.sub(pattern, '', text)
    
    text = text.strip()
    return text


def build_enhanced_prompt(system_prompt: str, user_prompt: str, context: Optional[str] = None) -> str:
    """
    Build a more structured prompt with better formatting for the model.
    """
    formatted_prompt = f"""<|system|>
{system_prompt}

You MUST:
1. Provide clear, factual information
2. Be concise and well-structured
3. Avoid speculation and unsupported claims
4. End with a complete thought
<|user|>
"""
    
    if context:
        formatted_prompt += f"Context: {context}\n\n"
    
    formatted_prompt += f"{user_prompt}\n<|assistant|>\n"
    
    return formatted_prompt


def build_chat_prompt(system_prompt: str, messages: List[ChatMessage]) -> str:
    """
    Convert structured chat messages into a single prompt
    compatible with llama.cpp-style models.
    """
    prompt = f"<|system|>\n{system_prompt}\n"

    for msg in messages:
        prompt += f"<|{msg.role}|>\n{msg.content}\n"

    prompt += "<|assistant|>\n"
    return prompt


def validate_prompt(prompt: str) -> bool:
    """
    Basic validation for prompts.
    """
    # Too short
    if len(prompt.strip()) < 5:
        return False
    
    # Mostly numbers/symbols
    if len([c for c in prompt if c.isalpha()]) < len(prompt) * 0.3:
        return False
    
    return True


# ==============================
# Routes
# ==============================

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "API is running"}


@app.post("/generate")
def generate(req: GenerateRequest):
    """
    Enhanced single-prompt text generation with better quality controls.
    """
    # Validate input
    if not validate_prompt(req.prompt):
        raise HTTPException(
            status_code=400,
            detail="Prompt is too short or contains mostly non-alphabetic characters"
        )
    
    request_id = str(uuid.uuid4())
    
    try:
        # Build enhanced prompt
        prompt = build_enhanced_prompt(SYSTEM_PROMPT, req.prompt, req.context)
        
        # Generate with better parameters for quality
        output = llm(
            prompt,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            top_k=req.top_k,
            top_p=req.top_p,
            stop=["<|user|>", "<|system|>", "\n\n"],  # Better stop sequences
            echo=False  # Don't echo the prompt
        )
        
        text = output["choices"][0]["text"]
        
        # Clean output
        text = clean_output(text)
        
        # Validation: reject if output is too short or empty
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=500,
                detail="Model generated invalid output. Try adjusting parameters."
            )
        
        response = {
            "request_id": request_id,
            "text": text,
            "tokens_used": output["usage"]["completion_tokens"],
            "model_info": {
                "temperature": req.temperature,
                "max_tokens": req.max_tokens,
                "top_k": req.top_k,
                "top_p": req.top_p
            }
        }
        
        if req.include_prompt:
            response["prompt"] = req.prompt
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


@app.post("/chat")
def chat(req: ChatRequest):
    """
    Multi-turn chat endpoint.
    Conversation memory is provided by the client.
    """
    request_id = str(uuid.uuid4())

    prompt = build_chat_prompt(SYSTEM_PROMPT, req.messages)

    output = llm(
        prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_k=req.top_k,
        top_p=req.top_p,
        stop=["<|user|>", "<|system|>"]
    )

    text = output["choices"][0]["text"]
    text = clean_output(text)

    return {
        "request_id": request_id,
        "text": text.strip(),
        "tokens_used": output["usage"]["completion_tokens"]
    }


@app.post("/generate/optimized")
def generate_optimized(req: GenerateRequest):
    """
    Optimized generation with better defaults for quality.
    Uses lower temperature and adjusted sampling for more consistent results.
    """
    # Override with optimized parameters for better quality
    optimized_req = GenerateRequest(
        prompt=req.prompt,
        context=req.context,
        max_tokens=min(req.max_tokens, 512),  # Cap at 512 for quality
        temperature=0.5,  # Lower for more coherent output
        top_k=30,  # More focused sampling
        top_p=0.85,  # Stricter nucleus sampling
        include_prompt=req.include_prompt
    )
    
    return generate(optimized_req)