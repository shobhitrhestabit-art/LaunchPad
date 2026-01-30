from ollama_client import call_llm

class SummarizerAgent:
    def __init__(self):
        self.memory = []
        self.system_prompt = (
            "You are a Summarizer Agent.\n"
            "Your ONLY task is to compress the given information.\n"
            "Do NOT add new facts.\n"
            "Do NOT answer the user."
        )

    def run(self, research_text: str) -> str:
        prompt = self._build_prompt(research_text)
        output = call_llm(prompt, max_tokens=250)
        self._update_memory(research_text, output)
        return output

    def _build_prompt(self, text: str) -> str:
        memory_context = "\n".join(self.memory[-10:])
        return f"""
SYSTEM:
{self.system_prompt}

CONTEXT:
{memory_context}

INPUT:
{text}

ASSISTANT:
"""

    def _update_memory(self, user, assistant):
        self.memory.append(f"INPUT: {user}")
        self.memory.append(f"ASSISTANT: {assistant}")
