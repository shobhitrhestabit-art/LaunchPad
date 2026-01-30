from agents.base_agent import BaseAgent
import json


class PlannerAgent(BaseAgent):
    """
    Planner Agent: Decomposes complex tasks into structured execution plans.
    
    Responsibilities:
    - Analyze user query and context
    - Create step-by-step execution plan
    - Assign tasks to appropriate agents
    - Structure plan for parallel/sequential execution
    
    Output Format: JSON with parallel_groups structure
    """
    
    def __init__(self):
        system_message = """You are an Expert Task Planner. Your role is to:
1. Analyze the user query carefully
2. Break it down into atomic tasks
3. Identify which agents should handle each task (Researcher, Analyst, Coder)
4. Structure tasks for optimal parallel execution
5. Return ONLY valid JSON, no other text or explanation

Guidelines:
- Researcher: Information gathering, research, fact-finding
- Analyst: Data analysis, trend analysis, strategic evaluation
- Coder: Implementation, debugging, technical solutions
- Prefer parallel execution when tasks are independent
- Put dependent tasks in sequential groups

Response MUST be ONLY this JSON structure, with no additional text:
{
  "parallel_groups": [
    [
      {"agent": "Researcher", "task": "specific research task"},
      {"agent": "Analyst", "task": "specific analysis task"}
    ],
    [
      {"agent": "Coder", "task": "specific coding task"}
    ]
  ]
}

CRITICAL: Return ONLY the JSON object. No markdown backticks, no explanation, no other text."""
        
        super().__init__("Planner", system_message)

    async def run(self, query: str) -> str:
        """
        Create execution plan for query.
        
        Args:
            query: User query with context
            
        Returns:
            JSON string with execution plan
        """
        response = await super().run(query)
        
        # Ensure we return the response as-is
        # The orchestrator will handle JSON extraction
        return response