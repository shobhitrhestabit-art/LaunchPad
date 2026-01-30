from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent

research_agent = ResearchAgent()
summarizer_agent = SummarizerAgent()
answer_agent = AnswerAgent()
print("Enter your research query:")
query = input("")

print("\nUSER QUERY:\n", query)

research_output = research_agent.run(query)
print("\nRESEARCH AGENT OUTPUT:\n", research_output)

summary = summarizer_agent.run(research_output)
print("\nSUMMARY OUTPUT:\n", summary)

final_answer = answer_agent.run(summary)
print("\nFINAL ANSWER:\n", final_answer)
