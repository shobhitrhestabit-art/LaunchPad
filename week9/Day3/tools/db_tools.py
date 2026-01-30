import sqlite3
from typing import List, Tuple, Any


def connect(db_path: str) -> sqlite3.Connection:
   
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to database: {e}") from e


def execute_query(
    conn: sqlite3.Connection,
    query: str,
    params: Tuple[Any, ...] = ()
) -> List[Tuple]:
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"SQL execution failed: {e}") from e


def execute_non_query(
    conn: sqlite3.Connection,
    query: str,
    params: Tuple[Any, ...] = ()
) -> None:
   
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"SQL write failed: {e}") from e
