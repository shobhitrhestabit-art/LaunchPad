# model_loader.py

from llama_cpp import Llama
from config import MODEL_PATH, CONTEXT_LENGTH, N_GPU_LAYERS



_llm = None


def load_model():
    """
    Load the GGUF model once and cache it.
    This function should be called only at app startup.
    """
    global _llm

    if _llm is None:
        print("Loading GGUF model from:", MODEL_PATH)

        _llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=CONTEXT_LENGTH,
            n_gpu_layers=N_GPU_LAYERS,
            verbose=False
        )

        print("GGUF model loaded successfully.")

    return _llm
