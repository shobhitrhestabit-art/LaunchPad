from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(Enum):
    FILE = "file"
    DB = "db"
    CODE = "code"


@dataclass
class Task:
    """
    Represents a single executable task in the orchestration pipeline.
    """
    id: str
    type: TaskType
    description: str

   
    depends_on: List[str] = field(default_factory=list)

   
    input: Dict[str, Any] = field(default_factory=dict)

   
    output: Optional[Any] = None

    
    status: TaskStatus = TaskStatus.PENDING
