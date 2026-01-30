import sqlite3
import logging
import os
from threading import Lock

logger = logging.getLogger(__name__)

class DBHandler:
    def __init__(self, db_path="memory/long_term.db"):
        self.db_path = db_path
        self.lock = Lock()  # Thread safety
        
       
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        
      
        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False,
            timeout=10.0  
        )
        
        
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")  
        
        self.create_table()
        logger.info(f"✓ Database initialized at {db_path}")

    def create_table(self):
        """Create memories table if it doesn't exist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS memories 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                               content TEXT NOT NULL,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            
            
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp 
                             ON memories(timestamp)''')
            
            self.conn.commit()
            logger.debug("✓ Table 'memories' ready")
            
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise

    def save_text(self, text):
        """
        Save interaction text to database
        
        Args:
            text: String to save
        
        Returns:
            Integer ID of inserted row
        """
        try:
            if not text or not text.strip():
                logger.warning("Attempted to save empty text")
                return None
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO memories (content) VALUES (?)", (text,))
                self.conn.commit()
                new_id = cursor.lastrowid
                logger.debug(f"✓ Text saved with ID: {new_id}")
                return new_id
                
        except Exception as e:
            logger.error(f"Error saving text: {e}")
            raise

    def get_text_by_ids(self, ids):
        """
        Retrieve text by IDs
        
        Args:
            ids: List of integer IDs
        
        Returns:
            String with all retrieved content, separated by newlines
        """
        try:
            if not ids or (isinstance(ids, list) and ids[0] == -1):
                logger.debug("No valid IDs to retrieve")
                return ""
            
            # Ensure ids is a list
            if not isinstance(ids, list):
                ids = [ids]
            
            with self.lock:
                cursor = self.conn.cursor()
                placeholders = ', '.join(['?'] * len(ids))
                cursor.execute(
                    f"SELECT id, content FROM memories WHERE id IN ({placeholders}) ORDER BY id DESC",
                    ids
                )
                rows = cursor.fetchall()
                
                if not rows:
                    logger.debug(f"No content found for IDs: {ids}")
                    return ""
                
                # Format with ID for context
                result = "\n".join([f"[Memory {r[0]}]: {r[1]}" for r in rows])
                logger.debug(f"✓ Retrieved {len(rows)} memories")
                return result
                
        except Exception as e:
            logger.error(f"Error retrieving text: {e}")
            return ""
    
    def get_all_texts(self):
        """Get all stored memories (useful for rebuilding indexes)"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id, content FROM memories ORDER BY id ASC")
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error retrieving all texts: {e}")
            return []
    
    def delete_old_memories(self, days=30):
        """
        Delete memories older than N days to prevent unlimited growth
        
        Args:
            days: Number of days to keep
        """
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute(
                    "DELETE FROM memories WHERE timestamp < datetime('now', '-' || ? || ' days')",
                    (days,)
                )
                self.conn.commit()
                logger.info(f"✓ Deleted {cursor.rowcount} old memories")
                
        except Exception as e:
            logger.error(f"Error deleting old memories: {e}")
    
    def get_count(self):
        """Get total number of stored memories"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memories")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting count: {e}")
            return 0