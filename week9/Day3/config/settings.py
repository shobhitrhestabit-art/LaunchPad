from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



CSV_PATH = DATA_DIR / "sales.csv"
DB_PATH = DATA_DIR / "sales.db"



INSIGHTS_PATH = OUTPUT_DIR / "insights.txt"



CSV_CHUNK_SIZE = 100_000




ORCHESTRATOR_LLM = "mistral"
CODE_AGENT_LLM = "llama3"
