import json
import os
from celery.result import AsyncResult
from fastapi import HTTPException
from redis import Redis

from ...entity.task import TaskEntity
# python3 -c "from redis import Redis ; client=Redis.from_url('redis://localhost:6379') ; print(client.keys())"
class TaskRepository:
    def __init__(self):
        redis_url = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
        self.client = Redis.from_url(redis_url)

    def create_task(self, task: TaskEntity) -> bool:
        """
        ta i pozostałe metody: go async?
        """
        task_id = task.id
        if self.client.get(task_id) == None: # or task.app.AsyncResult(task_id).ready() # https://derlin.github.io/introduction-to-fastapi-and-celery/03-celery/
            task_dict = task.__dict__.copy()
            # task_dict.pop('callable', None)
            self.client.set(task.id, json.dumps(task_dict))
        else:
            raise HTTPException(400, "Task with given id already exists")
        return True

    def update_task(self, task: TaskEntity) -> bool:
        # make sure task_id is not None
        existing_task = self.client.get(task.id)
        if not existing_task:
            raise HTTPException(404, "Task with given id doesn't exists")

        task_dict = task.__dict__.copy()
        # task_dict.pop('callable', None)
        self.client.set(task.id, json.dumps(task_dict))

        return True

    def get_task(self, task_id: str) -> TaskEntity | None:
        task = self.client.get(task_id)
        if not task:
            raise HTTPException(404, "Task with given id doesn't exists")
        return TaskEntity(**task) # nice

    # def get_task(self, task_id: str) -> dict | None:
    #     task_result = AsyncResult(task_id)
    #     if(task_result):
    #         return {'task_id': task_id, 'status': task_result.status, 'result': task_result.result}
    #     else:
    #         None
