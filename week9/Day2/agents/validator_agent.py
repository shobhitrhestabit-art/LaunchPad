from autogen import AssistantAgent
from llm_config import llm_config


class ValidatorAgent:
    """
    Validator Agent
    - Checks the refined answer for correctness and completeness
    - Acts as a quality gate before final output
    """

    def __init__(self):
        self.agent = AssistantAgent(
            name="Validator",
            system_message=(
                "You are a Validator agent.\n"
                "Your job is to check the answer for correctness, completeness, and clarity.\n"
                "Rules:\n"
                "1. If the answer is acceptable, reply with 'APPROVED'.\n"
                "2. If not, reply with 'REJECTED' and briefly state the issues.\n"
                "3. Do NOT rewrite the answer."
            ),
            llm_config=llm_config
        )

    def validate(self, answer: str) -> str:
        """
        Validates the final refined answer.
        """

        response = self.agent.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Validate the following answer:\n\n"
                        f"{answer}"
                    ),
                }
            ]
        )

        return response
