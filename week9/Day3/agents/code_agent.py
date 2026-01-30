from llm.llama3_client import Llama3Client
from config.prompts import CODE_AGENT_SYSTEM_PROMPT


class CodeAgent:
    """
    Production-grade Code Agent.
    - Data-driven
    - Intent-aware
    - LLM used ONLY for rewriting
    """

    def __init__(self):
        self.llm = Llama3Client()

    def execute(self, task_input: dict, context: dict):
        intent = task_input.get("intent")
        rows = context.get("run_sql_queries")

      
        print("\n" + "="*50)
        print("DEBUG: CodeAgent.execute()")
        print("="*50)
        print(f"Intent: {intent}")
        print(f"Rows type: {type(rows)}")
        print(f"Rows value: {rows}")
        if rows:
            print(f"Number of rows: {len(rows)}")
            print(f"First row: {rows[0] if rows else 'N/A'}")
            print(f"First row length: {len(rows[0]) if rows else 'N/A'}")
        print("="*50 + "\n")

        if not rows:
            return ["No data available for analysis."]

       
        facts = []

        try:
            if intent == "TOP_BUYERS":
                for row in rows:
                    if len(row) >= 2:
                        buyer, revenue = row[0], row[1]
                        facts.append(
                            f"Buyer {buyer} generated total revenue of {revenue}."
                        )

            elif intent == "TOP_PRODUCTS":
                for row in rows:
                    if len(row) >= 2:
                        product, revenue = row[0], row[1]
                        facts.append(
                            f"Product '{product}' generated revenue of {revenue}."
                        )

            elif intent == "TOP_REGIONS":
                for row in rows:
                    if len(row) >= 2:
                        region, revenue = row[0], row[1]
                        facts.append(
                            f"Region '{region}' contributed {revenue} in sales."
                        )

            else:  # GENERAL_INSIGHTS
                for row in rows:
                    if len(row) >= 2:
                        product, revenue = row[0], row[1]
                        facts.append(
                            f"Product '{product}' is among the top revenue generators ({revenue})."
                        )

        except (IndexError, ValueError) as e:
            print(f" Error processing rows: {e}")
            return [f"Error processing data: {e}. Rows received: {rows}"]

        print(f" Generated {len(facts)} facts")
        if facts:
            print("First fact:", facts[0])

        if not facts:
            return ["No valid data to generate insights."]

       
        prompt = (
            CODE_AGENT_SYSTEM_PROMPT
            + "\nRewrite the following facts into clear business insights:\n\n"
            + "\n".join(facts)
        )

        try:
            print(" Calling Llama3 for rewriting...")
            rewritten = self.llm.generate(prompt)

            # If LLM fails, return raw facts (safe fallback)
            if not rewritten or not rewritten.strip():
                print(" LLM returned empty, using raw facts")
                return facts

            result = [
                line.strip()
                for line in rewritten.split("\n")
                if line.strip()
            ]
            
            print(f" LLM generated {len(result)} insights")
            return result
            
        except Exception as e:
            print(f" LLM failed: {e}, using raw facts")
           
            return facts