# config.py - IMPROVED VERSION

# ==============================
# Model Configuration
# ==============================

# Path to quantised GGUF model
MODEL_PATH = "../models/model-q4_0.gguf"

# Context window (tokens)
CONTEXT_LENGTH = 2048

# Number of GPU layers to offload
# Set to 0 for CPU-only
# Typical values:
#   CPU-only  → 0
#   T4 / P100 → 20–40
N_GPU_LAYERS = 35


# ==============================
# Generation Defaults (IMPROVED)
# ==============================

# For general prompts - balanced quality and speed
DEFAULT_MAX_TOKENS = 256
DEFAULT_TEMPERATURE = 0.6  # Reduced from 0.7 for more coherent output
DEFAULT_TOP_K = 35  # Reduced from 40 for focused sampling
DEFAULT_TOP_P = 0.85  # Reduced from 0.9 for more deterministic output

# Alternative presets for different use cases
GENERATION_PRESETS = {
    "precise": {
        "temperature": 0.3,
        "top_k": 20,
        "top_p": 0.8,
        "max_tokens": 256
    },
    "balanced": {
        "temperature": 0.6,
        "top_k": 35,
        "top_p": 0.85,
        "max_tokens": 256
    },
    "creative": {
        "temperature": 0.9,
        "top_k": 50,
        "top_p": 0.95,
        "max_tokens": 512
    },
    "concise": {
        "temperature": 0.5,
        "top_k": 30,
        "top_p": 0.8,
        "max_tokens": 150
    }
}


# ==============================
# API Server Configuration
# ==============================

HOST = "0.0.0.0"
PORT = 8000


# ==============================
# System Prompt (Health Domain) - IMPROVED
# ==============================

SYSTEM_PROMPT = (
    "You are a knowledgeable health and medical information assistant. "
    "Your role is to provide clear, accurate, factual, and evidence-based information. "
    "Always:\n"
    "- Be precise and cite common medical knowledge when relevant\n"
    "- Avoid speculation, opinions, or unsupported claims\n"
    "- Keep responses concise and well-organized\n"
    "- Use simple language that is easy to understand\n"
    "- Recommend consulting healthcare professionals for medical advice\n"
    "- Do not diagnose or prescribe treatment"
)