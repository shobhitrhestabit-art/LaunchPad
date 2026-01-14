import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "netflix.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "netflix_titles.csv")
TABLE_NAME = "netflix"

def load_csv_to_db():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()

    print("CSV loaded into database table:", TABLE_NAME)
    print("DB PATH USED (csv_to_db):", DB_PATH)
