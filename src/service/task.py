from datetime import datetime

from celery.result import AsyncResult

from ..entity.task import TaskResult, TaskStatus
from ..repository.redis.task import TaskRepository
from ..worker import create_task


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    async def get_task(self, task_id: str) -> dict:
        """Retrieves task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: The task.
        """
        task = self.task_repository.get_task(task_id)
        return task

    async def get_task_status(self, task_id: str) -> TaskStatus:
        """Retrieves the status of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The current status of the task.
        """
        task = self.task_repository.get_task(task_id)
        return task['status']

    async def get_task_result(self, task_id: str) -> TaskResult | None:
        """Retrieves the result of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The result of the task.
        """
        task = self.task_repository.get_task(task_id)
        return task['result']

    #TODO zmienić aby przekazywać coś innego niż int
    async def create_task(self, task_type: int) -> str:
        """Creates a new task.

        Returns:
            str: The unique identifier of the newly created task.
        """
        new_task = create_task.delay(task_type)
        return new_task.id
