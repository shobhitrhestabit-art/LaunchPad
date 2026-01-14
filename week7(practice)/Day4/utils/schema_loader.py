import sqlite3

def load_schema(db_path):
    print("DB PATH USED (schema_loader):", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        cols = cursor.fetchall()

        schema[table] = [
            {"column": c[1], "type": c[2]}
            for c in cols
        ]

    conn.close()
    return schema
