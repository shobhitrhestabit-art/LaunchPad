from ollama_client import call_llm

class AnswerAgent:
    def __init__(self):
        self.memory = []
        self.system_prompt = (
            "You are an Answer Agent.\n"
            "Your job is to produce the final user-facing answer.\n"
            "Use ONLY the provided summary."
        )

    def run(self, summary: str) -> str:
        prompt = self._build_prompt(summary)
        output = call_llm(prompt, max_tokens=300)
        self._update_memory(summary, output)
        return output

    def _build_prompt(self, summary: str) -> str:
        memory_context = "\n".join(self.memory[-10:])
        return f"""
SYSTEM:
{self.system_prompt}

CONTEXT:
{memory_context}

SUMMARY:
{summary}

ASSISTANT:
"""

    def _update_memory(self, user, assistant):
        self.memory.append(f"SUMMARY: {user}")
        self.memory.append(f"ASSISTANT: {assistant}")
