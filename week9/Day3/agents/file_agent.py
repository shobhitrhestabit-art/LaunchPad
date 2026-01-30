import csv
from pathlib import Path


class FileAgent:
    """
    Production-grade File Agent.
    """

    def execute(self, task_input: dict):
        print(f"[FILE_AGENT.execute] Called with input: {task_input}")
        
        if "file_path" not in task_input:
            raise ValueError("FileAgent requires 'file_path' in task_input")

        path = Path(task_input["file_path"])
        print(f"[FILE_AGENT.execute] Target file: {path}")

        if not path.exists():
            print(f"[FILE_AGENT.execute]  File not found: {path}")
            raise FileNotFoundError(f"CSV file not found: {path}")

        print(f"[FILE_AGENT.execute] File exists, reading CSV...")
        rows = []

        try:
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, 1):
                    rows.append(row)
                    if i <= 3:
                        print(f"[FILE_AGENT.execute]   Row {i}: {row}")
            
            print(f"[FILE_AGENT.execute]  Read {len(rows)} rows from CSV")
                        
        except Exception as e:
            print(f"[FILE_AGENT.execute]  Failed to read CSV: {e}")
            raise RuntimeError(f"Failed to read CSV file: {e}") from e

        if not rows:
            print(f"[FILE_AGENT.execute]  CSV file is empty")
            raise ValueError("CSV file is empty or unreadable")

        return rows