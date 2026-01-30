import asyncio

from orchestrator.planner import PlannerAgent
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator_agent import ValidatorAgent



async def run_workers(tasks):
    workers = [WorkerAgent(name=f"Worker-{i+1}") for i in range(len(tasks))]

    coroutines = [
        asyncio.to_thread(worker.run, task)
        for worker, task in zip(workers, tasks)
    ]

    results = await asyncio.gather(*coroutines)
    return {tasks[i]: results[i] for i in range(len(tasks))}


def main():
    print("===== DAY 2 : MULTI-AGENT ORCHESTRATION =====\n")

    
    user_query = input("Enter your query: ").strip()
    print("\nUSER QUERY:\n", user_query)

   
    planner = PlannerAgent()
    tasks = planner.create_tasks(user_query)

    print("\nTASKS CREATED BY PLANNER:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    
    print("\nRUNNING WORKER AGENTS IN PARALLEL...\n")
    worker_outputs = asyncio.run(run_workers(tasks))

    
    reflection_agent = ReflectionAgent()
    refined_answer = reflection_agent.reflect(worker_outputs)

    print("\nREFINED ANSWER:\n")
    print(refined_answer)

   
    validator_agent = ValidatorAgent()
    validation_result = validator_agent.validate(refined_answer)

    print("\nVALIDATION RESULT:\n", validation_result)

   
    if "APPROVED" in validation_result.upper():
        print("\nFINAL ANSWER (APPROVED):\n")
        print(refined_answer)
    else:
        print("\n ANSWER REJECTED BY VALIDATOR")
        print("Issues:\n", validation_result)


if __name__ == "__main__":
    main()
