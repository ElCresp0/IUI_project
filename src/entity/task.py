from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable


DATEFORMAT = "%Y-%m-%dT%H:%M:%S"

class TaskMode(str, Enum):
    ZERO_SHOT = 0
    FEW_SHOT = 1


class Framework(str, Enum):
    STORMTROOPER = 'stormtrooper'
    BULLET = 'bullet'
    TARS = 'tars'


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
    THIS MIGHT BE A BIT OUTDATED

    represents a text classification task
    mode, callable and args fields are necessary
    to create a celery coroutine to delegate the task
    """
    id: str | None
    start_time: str
    end_time: str | None = None
    mode: TaskMode | None = None
    framework: Framework | None = None
    args: str | None = None # JSON serialized dict
    status: TaskStatus | None = None
    result: TaskResult | None = None
