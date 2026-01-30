from typing import Dict, Any
from orchestrator.task_schema import TaskType, TaskStatus
from orchestrator.task_planner import TaskPlanner

from agents.file_agent import FileAgent
from agents.db_agent import DBAgent
from agents.code_agent import CodeAgent


class Orchestrator:
    """
    Production-grade Orchestrator.
    """

    def __init__(self):
        print("[ORCHESTRATOR] Initializing agents...")
        self.file_agent = FileAgent()
        self.db_agent = DBAgent()
        self.code_agent = CodeAgent()
        print("[ORCHESTRATOR] All agents initialized")

    def run(self, user_prompt: str):
        print(f"[ORCHESTRATOR] Starting orchestration for: '{user_prompt}'")
        
        # Reset context PER RUN
        self.context: Dict[str, Any] = {}
        print("[ORCHESTRATOR] Context reset")

        print("[ORCHESTRATOR] Initializing task planner...")
        planner = TaskPlanner()
        
        print("[ORCHESTRATOR] Calling planner.plan()...")
        tasks = planner.plan(user_prompt)
        print(f"[ORCHESTRATOR] Received {len(tasks)} tasks from planner")
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[ORCHESTRATOR] Task {i}/{len(tasks)}: {task.id} ({task.type})")
            print(f"[ORCHESTRATOR]   Description: {task.description}")
            print(f"[ORCHESTRATOR]   Dependencies: {task.depends_on}")
            self._execute_task(task)
            print(f"[ORCHESTRATOR]   Status: {task.status}")

        print(f"\n[ORCHESTRATOR] All tasks completed")
        print(f"[ORCHESTRATOR] Returning output from final task: {tasks[-1].id}")
        return tasks[-1].output

    def _execute_task(self, task):
        print(f"[ORCHESTRATOR._execute_task] Checking dependencies for '{task.id}'...")
        
        # Dependency check
        for dep in task.depends_on:
            if dep not in self.context:
                task.status = TaskStatus.FAILED
                print(f"[ORCHESTRATOR._execute_task]  Dependency '{dep}' not satisfied")
                raise RuntimeError(
                    f"Dependency '{dep}' not satisfied for task '{task.id}'"
                )
            print(f"[ORCHESTRATOR._execute_task]   ✓ Dependency '{dep}' satisfied")

        task.status = TaskStatus.RUNNING
        print(f"[ORCHESTRATOR._execute_task] Executing task '{task.id}'...")

        try:
            # -------- ROUTING --------
            if task.type == TaskType.FILE:
                print(f"[ORCHESTRATOR._execute_task] Routing to FileAgent")
                result = self.file_agent.execute(task.input)

            elif task.type == TaskType.DB:
                print(f"[ORCHESTRATOR._execute_task] Routing to DBAgent")
                result = self.db_agent.execute(
                    task_input=task.input,
                    context=self.context
                )

            elif task.type == TaskType.CODE:
                print(f"[ORCHESTRATOR._execute_task] Routing to CodeAgent")
                result = self.code_agent.execute(
                    task_input=task.input,
                    context=self.context
                )

            else:
                raise ValueError(f"Unknown task type: {task.type}")
            # ------------------------

            print(f"[ORCHESTRATOR._execute_task] Task '{task.id}' completed successfully")
            print(f"[ORCHESTRATOR._execute_task] Result type: {type(result)}")
            
            task.output = result
            self.context[task.id] = result
            task.status = TaskStatus.COMPLETED
            
            print(f"[ORCHESTRATOR._execute_task] Added '{task.id}' to context")

        except Exception as e:
            task.status = TaskStatus.FAILED
            print(f"[ORCHESTRATOR._execute_task] Task '{task.id}' failed: {e}")
            raise RuntimeError(
                f"Task '{task.id}' failed: {e}"
            ) from e