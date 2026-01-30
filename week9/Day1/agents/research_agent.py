from ollama_client import call_llm

class ResearchAgent:
    def __init__(self):
        self.memory = []
        self.system_prompt = (
            "You are a Research Agent.\n"
            "Your ONLY task is to gather factual and detailed information.\n"
            "Do NOT summarize.\n"
            "Do NOT give a final answer."
        )

    def run(self, user_query: str) -> str:
        prompt = self._build_prompt(user_query)
        output = call_llm(prompt, max_tokens=400)
        self._update_memory(user_query, output)
        return output

    def _build_prompt(self, user_query: str) -> str:
        memory_context = "\n".join(self.memory[-10:])
        return f"""
SYSTEM:
{self.system_prompt}

CONTEXT:
{memory_context}

USER:
{user_query}

ASSISTANT:
"""

    def _update_memory(self, user, assistant):
        self.memory.append(f"USER: {user}")
        self.memory.append(f"ASSISTANT: {assistant}")
