import os 
import sqlite3
from utils.csv_to_db import load_csv_to_db
from utils.schema_loader import load_schema
from generator.sql_generator import generate_sql


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "netflix.db")


def execute_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description]

    conn.close()
    return columns, rows

def main():
    

    # Step 1: Load CSV → DB (one-time)
    load_csv_to_db()

    # Step 2: Load schema
    schema = load_schema(DB_PATH)

    print("Database Schema:")
    print(schema)

    question = input("Ask your SQL question: ")

    # Step 3: Generate SQL
    sql = generate_sql(question, schema)
    print("\nGenerated SQL:\n", sql)

    # Step 4: Execute SQL
    columns, rows = execute_sql(sql)

    print("\nResult:")
    print(columns)
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
