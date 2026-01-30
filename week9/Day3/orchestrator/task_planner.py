from orchestrator.task_schema import Task, TaskType
from config.settings import CSV_PATH
from llm.mistral_client import MistralClient
from config.prompts import ORCHESTRATOR_SYSTEM_PROMPT, ORCHESTRATOR_TASK_PROMPT


class TaskPlanner:
    """
    Production-grade Task Planner.
    - Uses LLM for intent classification
    - Explicit task dependencies
    - Flexible to handle new intents
    """

    def __init__(self):
        self.llm = MistralClient()

    def plan(self, user_prompt: str):
        if not user_prompt or not user_prompt.strip():
            raise ValueError("User prompt cannot be empty")

        
        full_prompt = (
            ORCHESTRATOR_SYSTEM_PROMPT + "\n\n" +
            ORCHESTRATOR_TASK_PROMPT.format(user_prompt=user_prompt)
        )

        llm_response = self.llm.generate(full_prompt)
        
        
        intent = self._parse_intent(llm_response, user_prompt)
        
        # --------------------------------------

        return [
            Task(
                id="read_csv",
                type=TaskType.FILE,
                description="Read sales CSV file",
                input={"file_path": str(CSV_PATH)}
            ),
            Task(
                id="load_sqlite",
                type=TaskType.DB,
                description="Load CSV data into SQLite",
                depends_on=["read_csv"]
            ),
            Task(
                id="run_sql_queries",
                type=TaskType.DB,
                description=f"Run SQL queries for intent {intent}",
                depends_on=["load_sqlite"],
                input={"intent": intent}
            ),
            Task(
                id="generate_insights",
                type=TaskType.CODE,
                description="Generate business insights",
                depends_on=["run_sql_queries"],
                input={"intent": intent}
            )
        ]

    def _parse_intent(self, llm_response: str, user_prompt: str) -> str:
        """
        Parse intent from LLM response with fallback to keyword matching
        """
        response_lower = llm_response.lower()
        prompt_lower = user_prompt.lower()
        
        if "top_buyers" in response_lower or "buyer" in response_lower:
            return "TOP_BUYERS"
        elif "top_products" in response_lower or "product" in response_lower:
            return "TOP_PRODUCTS"
        elif "top_regions" in response_lower or "region" in response_lower:
            return "TOP_REGIONS"
        
        
        if "buyer" in prompt_lower or "customer" in prompt_lower:
            return "TOP_BUYERS"
        elif "product" in prompt_lower:
            return "TOP_PRODUCTS"
        elif "region" in prompt_lower:
            return "TOP_REGIONS"
        else:
            return "GENERAL_INSIGHTS"