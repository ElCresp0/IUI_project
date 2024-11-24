from fastapi import BackgroundTasks

from ..service.task import TaskService


def _zero_shot_classification(path_model, user_option, id, task_service: TaskService):
    pass
    # TODO here add logic for stormtrooper

    # TODO here we can add some additional notification
    # https://fastapi.tiangolo.com/tutorial/background-tasks/


def _few_shot_classification():
    pass


class StormtrooperService:
    def __init__(self):
        self.task_service = TaskService()

    def add_zero_shot(self, path_model, user_option, background_tasks: BackgroundTasks):
        #TODO jakoś przekazać zadanie do workera - może przekazać funkcje?
        task_type = 1
        id = self.task_service.create_task(task_type)

        #background_tasks.add_task(_zero_shot_classification, path_model, user_option, id, self.task_service)

        return id
