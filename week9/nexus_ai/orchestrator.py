import asyncio
import json
import re
from logger import log
from memory.memory_manager import MemoryManager

from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.coder import CoderAgent
from agents.critic import CriticAgent
from agents.optimizer import OptimizerAgent
from agents.validator import ValidatorAgent
from agents.reporter import ReporterAgent

class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.coder = CoderAgent()
        self.critic = CriticAgent()
        self.optimizer = OptimizerAgent()
        self.validator = ValidatorAgent()
        self.reporter = ReporterAgent()

        self.agent_map = {
            "Researcher": self.researcher,
            "Analyst": self.analyst,
            "Coder": self.coder,
        }

    async def run_parallel(self, tasks):
        """Execute multiple agent tasks in parallel safely"""
        return await asyncio.gather(*[
            agent.run(task) for agent, task in tasks
        ], return_exceptions=True)

    def _extract_json(self, text: str) -> dict:
        """
        Robustly extract JSON from text that may contain other content.
        Tries multiple strategies:
        1. Find JSON block between {} or []
        2. Use regex to extract JSON
        3. Return fallback structure
        """
        text = text.strip()
        
       
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                json_str = text[start_idx:end_idx + 1]
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                log("ORCHESTRATOR", f"JSON parse error in strategy 1: {e}")
        
        
        json_pattern = r'\{[^{}]*"parallel_groups"[^{}]*\[[\s\S]*\]\s*\}'
        match = re.search(json_pattern, text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                log("ORCHESTRATOR", f"JSON parse error in strategy 2: {e}")
        
        
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
        
       
        log("ORCHESTRATOR", "Failed to extract JSON, using default plan")
        return {
            "parallel_groups": [
                [
                    {"agent": "Researcher", "task": text[:500]},
                    {"agent": "Analyst", "task": f"Analyze: {text[:500]}"}
                ]
            ]
        }

    async def run(self, query: str):
        """Main orchestration loop"""
        log("ORCHESTRATOR", f"Query received: {query[:50]}...")
        
        try:
            context = self.memory.recall(query)
        except Exception as e:
            log("ORCHESTRATOR", f"Memory recall failed: {e}")
            context = ""

        planner_prompt = f"""USER QUERY: {query}

RELEVANT CONTEXT: {context}

Create execution plan. Return ONLY JSON with this structure:
{{
  "parallel_groups": [
    [
      {{"agent": "Researcher", "task": "..."}},
      {{"agent": "Analyst", "task": "..."}}
    ]
  ]
}}

Return ONLY the JSON, no other text."""
        
        
        log("ORCHESTRATOR", "Requesting plan from PlannerAgent...")
        plan_raw = await self.planner.run(planner_prompt)
        log("ORCHESTRATOR", f"Planner response: {plan_raw[:200]}...")
        
       
        try:
            plan = self._extract_json(plan_raw)
        except Exception as e:
            log("ORCHESTRATOR", f"JSON extraction failed: {e}")
            return f" Error: Failed to parse planner response. Detail: {e}"

        results = {}

        # Execute Parallel Groups
        try:
            for group_idx, group in enumerate(plan.get("parallel_groups", [])):
                log("ORCHESTRATOR", f"Executing parallel group {group_idx + 1}")
                
                batch = [
                    (self.agent_map[step["agent"]], step["task"])
                    for step in group if step.get("agent") in self.agent_map
                ]

                if not batch:
                    log("ORCHESTRATOR", f"Group {group_idx + 1} has no valid agents")
                    continue
                
                outputs = await self.run_parallel(batch)

                for step, output in zip(group, outputs):
                    agent_name = step.get("agent", "Unknown")
                    if isinstance(output, Exception):
                        error_msg = f"Task failed: {str(output)}"
                        results[agent_name] = error_msg
                        log("ORCHESTRATOR", error_msg)
                    else:
                        results[agent_name] = output
                        log("ORCHESTRATOR", f"{agent_name} completed")
                        try:
                            self.memory.add_long_term(output)
                        except Exception as e:
                            log("ORCHESTRATOR", f"Memory storage failed: {e}")
        except Exception as e:
            log("ORCHESTRATOR", f"Parallel execution failed: {e}")
            return f" Error during execution: {str(e)}"

        # Sequential Refinement Loop
        try:
            log("ORCHESTRATOR", "Running critic...")
            critique = await self.critic.run(json.dumps(results))
            
            log("ORCHESTRATOR", "Running optimizer...")
            optimized = await self.optimizer.run(critique)
            
            log("ORCHESTRATOR", "Running validator...")
            await self.validator.run(optimized)

            log("ORCHESTRATOR", "Running reporter...")
            final = await self.reporter.run(optimized)
            
            try:
                self.memory.add_long_term(final)
            except Exception as e:
                log("ORCHESTRATOR", f"Final memory storage failed: {e}")

            return final
        except Exception as e:
            log("ORCHESTRATOR", f"Refinement loop failed: {e}")
            return f" Error in refinement: {str(e)}"