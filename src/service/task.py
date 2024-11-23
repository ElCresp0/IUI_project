from datetime import datetime

from ..entity.task import TaskEntity, TaskResult, TaskStatus
from ..repository.task import TaskRepository


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    async def get_task_status(self, task_id: str) -> TaskStatus:
        """Retrieves the status of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The current status of the task.
        """
        task = await self.task_repository.get_task(task_id)
        if not task:
            raise Exception(f'Task with id {task_id} not found.')
        return task.status

    async def get_task_result(self, task_id: str) -> TaskResult | None:
        """Retrieves the result of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The result of the task.
        """
        task = await self.task_repository.get_task(task_id)
        if not task:
            raise Exception(f'Task with id {task_id} not found.')
        return task.result

    async def create_task(self) -> str:
        """Creates a new task in the 'PENDING' state.

        Returns:
            str: The unique identifier of the newly created task.
        """
        print('x')
        new_task = TaskEntity(id='', start_time=datetime.now(), end_time=None, status=TaskStatus.PENDING, result=None)
        print('y')
        return await self.task_repository.create_task(new_task)

    async def delete_task(self, task_id: str):
        """Deletes a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        """
        success = await self.task_repository.remove_task(task_id)
        if not success:
            raise Exception(f'Failed to delete task with id {task_id}.')

    async def start_task(self, task_id: str):
        """Starts a task by updating its status to 'IN_PROGRESS'.

        Args:
            task_id (str): The unique identifier of the task.

        """
        task = await self.task_repository.get_task(task_id)
        if not task:
            raise Exception(f'Task with id {task_id} not found.')
        if task.status != TaskStatus.PENDING:
            raise Exception("Task can only be started if it is in 'PENDING' status.")

        task.status = TaskStatus.IN_PROGRESS
        success = await self.task_repository.update_task(task_id, task)
        if not success:
            raise Exception(f'Failed to update task with id {task_id}.')

    async def finish_task(self, task_id: str, result: TaskResult):
        """Completes a task by updating its status to 'COMPLETED' and updating result.

        Args:
            task_id (str): The unique identifier of the task.
            result (TaskResult): The unique identifier of the task.

        """
        task = await self.task_repository.get_task(task_id)
        if not task:
            raise Exception(f'Task with id {task_id} not found.')
        if task.status != TaskStatus.IN_PROGRESS:
            raise Exception("Task can only be finished if it is in 'IN_PROGRESS' status.")

        task.status = TaskStatus.COMPLETED
        task.result = result
        task.end_time = datetime.now()
        success = await self.task_repository.update_task(task_id, task)
        if not success:
            raise Exception(f'Failed to update task with id {task_id}.')
