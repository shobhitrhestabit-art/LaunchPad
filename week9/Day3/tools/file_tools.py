import csv
from pathlib import Path
from typing import List, Dict


def read_csv(file_path: str) -> List[Dict[str, str]]:
    
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows: List[Dict[str, str]] = []

    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV file: {e}") from e

    if not rows:
        raise ValueError("CSV file is empty")

    return rows
