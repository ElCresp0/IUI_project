from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable


class TaskMode(str, Enum):
    ZERO_SHOT = 0
    FEW_SHOT = 1


class TaskStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


# TODO Change ENUM class to class with real result from model
class TaskResult(str, Enum):
    SUCCEED = 'succeed'
    FAILED = 'failed'


@dataclass
class TaskEntity:
    """
    represents a text classification task
    mode, callable and args fields are necessary
    to create a celery coroutine to delegate the task
    """
    id: str | None
    start_time: datetime
    end_time: datetime | None = None
    mode: TaskMode | None = None
    callable: Callable | None = None # framework dependent callable
    args: dict = {}                  # framework and mode dependent args
    status: TaskStatus | None = None
    result: TaskResult | None = None
