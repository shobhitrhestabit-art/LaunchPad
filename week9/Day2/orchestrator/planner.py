from autogen import AssistantAgent
from llm_config import llm_config


class PlannerAgent:
    """
    Planner / Orchestrator Agent
    - Receives the user query
    - Decomposes it into independent tasks (DAG)
    - Does NOT execute tasks
    """

    def __init__(self):
        self.agent = AssistantAgent(
            name="Planner",
            system_message=(
                "You are a Planner agent.\n"
                "Your job is to break the user query into independent, parallelizable tasks.\n"
                "Rules:\n"
                "1. Do NOT answer the question.\n"
                "2. Do NOT explain tasks.\n"
                "3. Return tasks as a numbered list.\n"
                "4. Each task must be independent.\n"
            ),
            llm_config=llm_config
        )

    def create_tasks(self, user_query: str) -> list[str]:
        """
        Takes a user query and returns a list of tasks.
        """

        response = self.agent.generate_reply(
            messages=[
                {"role": "user", "content": user_query}
            ]
        )

        
        tasks = []
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue

            
            if line[0].isdigit():
                line = line.lstrip("0123). ").strip()

            if line:
                tasks.append(line)

        return tasks
