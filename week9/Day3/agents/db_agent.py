import sqlite3
from config.settings import DB_PATH


class DBAgent:
    """
    Production-ready DB agent.
    """

    def __init__(self):
        self.db_path = DB_PATH
        print(f"[DB_AGENT.__init__] Database path: {self.db_path}")

    def execute(self, task_input: dict, context: dict):
        """
        Entry point called by Orchestrator
        """
        print(f"[DB_AGENT.execute] Called with task_input: {task_input}")
        print(f"[DB_AGENT.execute] Context keys: {list(context.keys())}")
        
        intent = task_input.get("intent")
        
        if intent:
            # This is a QUERY task
            print(f"[DB_AGENT.execute] Mode: QUERY (intent='{intent}')")
            result = self._query(intent)
            print(f"[DB_AGENT.execute]  Query returned {len(result)} rows")
            if result:
                print(f"[DB_AGENT.execute]   First row: {result[0]}")
            return result
        else:
            # This is a LOAD task
            print(f"[DB_AGENT.execute] Mode: LOAD")
            if "read_csv" not in context:
                print(f"[DB_AGENT.execute]  CSV data not found in context")
                raise ValueError("Cannot load database: CSV data not found in context")
            
            csv_data = context["read_csv"]
            print(f"[DB_AGENT.execute] Found {len(csv_data)} rows in context['read_csv']")
            result = self._load(csv_data)
            print(f"[DB_AGENT.execute]  {result}")
            return result

    def _load(self, rows):
        print(f"[DB_AGENT._load] Loading {len(rows)} rows into database...")
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        print(f"[DB_AGENT._load] Creating table if not exists...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER,
                date TEXT,
                product TEXT,
                region TEXT,
                quantity INTEGER,
                revenue INTEGER
            )
        """)

        print(f"[DB_AGENT._load] Clearing existing data...")
        cur.execute("DELETE FROM sales")

        loaded = 0
        for i, r in enumerate(rows, 1):
            try:
                cur.execute(
                    "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        int(r["order_id"]),
                        r["date"],
                        r["product"],
                        r["region"],
                        int(r["quantity"]),
                        int(r["revenue"])
                    )
                )
                loaded += 1
                if i <= 3:
                    print(f"[DB_AGENT._load]   Inserted row {i}")
            except Exception as e:
                print(f"[DB_AGENT._load]  Failed to load row {r}: {e}")

        conn.commit()
        print(f"[DB_AGENT._load] Committed {loaded} rows")
        
        # Verify data was loaded
        cur.execute("SELECT COUNT(*) FROM sales")
        count = cur.fetchone()[0]
        print(f"[DB_AGENT._load]  Database now contains {count} rows")
        
        conn.close()
        return "DB loaded"

    def _query(self, intent: str):
        print(f"[DB_AGENT._query] Querying with intent: {intent}")
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        if intent == "TOP_BUYERS":
            print(f"[DB_AGENT._query] Running TOP_BUYERS query...")
            cur.execute("""
                SELECT order_id, SUM(revenue)
                FROM sales
                GROUP BY order_id
                ORDER BY SUM(revenue) DESC
                LIMIT 5
            """)
            result = cur.fetchall()

        elif intent == "TOP_PRODUCTS":
            print(f"[DB_AGENT._query] Running TOP_PRODUCTS query...")
            cur.execute("""
                SELECT product, SUM(revenue)
                FROM sales
                GROUP BY product
                ORDER BY SUM(revenue) DESC
                LIMIT 5
            """)
            result = cur.fetchall()

        elif intent == "TOP_REGIONS":
            print(f"[DB_AGENT._query] Running TOP_REGIONS query...")
            cur.execute("""
                SELECT region, SUM(revenue)
                FROM sales
                GROUP BY region
                ORDER BY SUM(revenue) DESC
                LIMIT 5
            """)
            result = cur.fetchall()

        else:  # GENERAL_INSIGHTS
            print(f"[DB_AGENT._query] Running GENERAL_INSIGHTS query...")
            cur.execute("""
                SELECT product, SUM(revenue)
                FROM sales
                GROUP BY product
                ORDER BY SUM(revenue) DESC
                LIMIT 5
            """)
            result = cur.fetchall()

        print(f"[DB_AGENT._query] Query returned {len(result)} rows")
        conn.close()
        return result