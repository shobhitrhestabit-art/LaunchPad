import json
import redis
from datetime import datetime
from typing import Dict, List

REDIS_URL = "redis://localhost:6379"
CHAT_TTL_SECONDS = 60 * 60      
MAX_MESSAGES = 5               

LOG_FILE_PATH = "src/logs/CHAT-LOGS.json"


redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True
)


class MemoryStore:
    """
    Handles:
    1. Short-term conversation memory (Redis)
    2. Persistent audit logging (Local file)
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_key = f"chat:{session_id}"

   
    def get_last_messages(self) -> List[Dict]:
        """
        Fetch last N chat messages for a session.
        Used before answering (for conversational continuity).
        """
        messages = redis_client.lrange(
            self.redis_key,
            -MAX_MESSAGES,
            -1
        )
        return [json.loads(m) for m in messages]

    def add_message(self, role: str, content: str):
        """
        Store a single chat message in Redis.
        Called AFTER evaluation passes (accept / warn).
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }

        redis_client.rpush(
            self.redis_key,
            json.dumps(message)
        )

        
        redis_client.expire(
            self.redis_key,
            CHAT_TTL_SECONDS
        )

    
    def log_interaction(self, record: Dict):
        """
        Persist interaction details for debugging, evaluation,
        and offline analysis. Always written (even for rejects).
        """
        record["session_id"] = self.session_id
        record["timestamp"] = datetime.utcnow().isoformat()

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
