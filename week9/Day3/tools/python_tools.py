from typing import Any, Callable, Dict


def safe_execute(
    func: Callable[..., Any],
    *args,
    **kwargs
) -> Any:
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Python execution failed: {e}") from e


def validate_keys(data: Dict, required_keys: list):
    
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise KeyError(f"Missing required keys: {missing}")
