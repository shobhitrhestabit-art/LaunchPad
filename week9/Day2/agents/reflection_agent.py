from autogen import AssistantAgent
from llm_config import llm_config


class ReflectionAgent:
    """
    Reflection Agent
    - Takes outputs from all worker agents
    - Merges them into one coherent answer
    - Improves clarity, structure, and flow
    - Does NOT add new information
    """

    def __init__(self):
        self.agent = AssistantAgent(
            name="Reflection",
            system_message=(
                "You are a Reflection agent.\n"
                "Your job is to combine multiple worker outputs into a single, clear, "
                "well-structured response.\n"
                "Rules:\n"
                "1. Do NOT add new facts.\n"
                "2. Do NOT contradict worker outputs.\n"
                "3. Remove redundancy.\n"
                "4. Improve clarity and logical flow."
            ),
            llm_config=llm_config
        )

    def reflect(self, worker_outputs: dict) -> str:
        """
        Combines and improves worker outputs.
        """

        combined_text = "\n\n".join(
            f"- {output}" for output in worker_outputs.values()
        )

        response = self.agent.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Combine the following worker outputs into a single coherent answer:\n\n"
                        f"{combined_text}"
                    ),
                }
            ]
        )

        return response
