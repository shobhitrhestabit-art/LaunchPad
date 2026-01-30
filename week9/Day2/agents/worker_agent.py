from autogen import AssistantAgent
from llm_config import llm_config


class WorkerAgent:
    """
    Worker Agent
    - Executes ONE assigned task
    - Has no knowledge of the full user query
    - Has no coordination with other workers
    """

    def __init__(self, name: str):
        self.agent = AssistantAgent(
            name=name,
            system_message=(
                "You are a Worker agent.\n"
                "Your ONLY job is to execute the given task.\n"
                "Rules:\n"
                "1. Focus strictly on the task provided.\n"
                "2. Do NOT answer the full user query.\n"
                "3. Do NOT mention other tasks or agents.\n"
                "4. Return a clear, factual response for this task only."
            ),
            llm_config=llm_config
        )

    def run(self, task: str) -> str:
        """
        Executes the assigned task and returns the result.
        """

        response = self.agent.generate_reply(
            messages=[
                {"role": "user", "content": task}
            ]
        )

        return response
