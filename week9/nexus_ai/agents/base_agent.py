import asyncio
import requests
from config import LLM_CONFIG


class BaseAgent:
    def __init__(self, name: str, system_message: str):
        self.name = name
        self.system_message = system_message
        self.base_url = LLM_CONFIG["base_url"]
        self.model = LLM_CONFIG["model"]
        self.temperature = LLM_CONFIG["temperature"]
        self.max_tokens = LLM_CONFIG["max_tokens"]

    async def run(self, task: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._call_ollama, task
        )

    def _call_ollama(self, task: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": task}
                ],
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            },
            timeout=300
        )

        response.raise_for_status()
        return response.json()["message"]["content"].strip()
