from fastapi import BackgroundTasks
from service.task import *


def _zero_shot_classification(path_model, user_option, id, task_service):
    task_service.start_task(id)

    # TODO here add logic for stormtrooper

    task_service.finish_task(id)

    # TODO here we can add some additional notification
    # https://fastapi.tiangolo.com/tutorial/background-tasks/


def _few_shot_classification():
    pass


class StormtrooperService:
    def __init__(self):
        self.task_service = TaskService()

    def add_zero_shot(self, path_model, user_option, background_tasks: BackgroundTasks):
        id = self.task_service.create_task()

        background_tasks.add_task(_zero_shot_classification, path_model, user_option, id, self.task_service)

        return id
