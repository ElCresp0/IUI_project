from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

#TODO Change ENUM class to class with real result from model
class TaskResult(str, Enum):
    SUCCEED = 'succeed'
    FAILED = 'failed'

@dataclass
class TaskEntity:
    id: str | None
    start_time: datetime
    end_time: datetime | None = None
    status: TaskStatus | None = None
    result: TaskResult | None = None
