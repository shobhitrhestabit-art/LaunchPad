"""
Configuration for NEXUS AI system.
Using LOCAL LLM via Ollama.
"""

LLM_CONFIG = {
    "provider": "ollama",
    "model": "mistral",      # or "tinyllama"
    "temperature": 0.7,
    "max_tokens": 2048,
    "base_url": "http://localhost:11434"
}

LOG_FILE = "nexus_ai.log"
LOG_LEVEL = "INFO"

MAX_PARALLEL_TASKS = 3
REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 3
