from agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """
    Researcher Agent: Gathers information, conducts analysis, and provides insights.
    
    Responsibilities:
    - Research topics and gather information
    - Synthesize findings from multiple sources
    - Identify key facts and patterns
    - Provide context and background
    - Support decision-making with evidence
    
    Output: Detailed research findings with sources and insights
    """
    
    def __init__(self):
        system_message = """You are an Expert Research Specialist. Your role is to:
1. Thoroughly research the assigned topic
2. Gather comprehensive information from various angles
3. Identify key findings, trends, and patterns
4. Synthesize insights from the research
5. Provide well-structured, evidence-based findings

Guidelines:
- Be thorough and systematic in research approach
- Look for primary sources and authoritative information
- Identify contradictions and different perspectives
- Synthesize findings into coherent narratives
- Cite sources when possible (e.g., "According to X...")
- Highlight key insights and their implications

Format your response as:
## Key Findings
[Your findings here]

## Patterns & Trends
[Important patterns you identified]

## Implications
[What this means or its significance]

## Recommendations for Further Analysis
[What should be explored next]"""
        
        super().__init__("Researcher", system_message)

    async def run(self, task: str) -> str:
        """
        Conduct research on assigned task.
        
        Args:
            task: Research task description
            
        Returns:
            Research findings and insights
        """
        return await super().run(task)