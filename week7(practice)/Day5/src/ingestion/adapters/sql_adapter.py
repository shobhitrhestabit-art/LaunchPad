import sqlite3
from src.ingestion.models import IngestDocument


def load_sql_schema(db_path: str):
    """
    Reads SQLite DB schema and returns one IngestDocument per table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = cursor.fetchall()

    documents = []

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        schema_text = f"Table: {table_name}\nColumns:\n"
        for col in columns:
            schema_text += f"- {col[1]} ({col[2]})\n"

        documents.append(
            IngestDocument(
                text=schema_text,
                source_type="sql",
                source_id=table_name,
                metadata={
                    "db": db_path
                }
            )
        )

    conn.close()
    return documents
