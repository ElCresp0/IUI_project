from fastapi import BackgroundTasks

from stormtrooper.set_fit import SetFitClassifier
from stormtrooper import ZeroShotClassifier

from ..service.task import TaskService
from ..entity.task import TaskMode, TaskStatus, TaskEntity
from .framework import Framework
from .model import ModelService

class StormtrooperService(Framework):
    def __init__(self):
        model_path = ModelService().get_sbert_base_cased_pl()
        self.few_shot_model = SetFitClassifier(model_path)

    def add_few_shot(self, args):
        """
        tworzy i przekazuje do workera-selera TaskEntity
        """
        taskEntity = TaskEntity(
            status = TaskStatus.PENDING,
            mode = TaskMode.ZERO_SHOT,
            callable = self._few_shot_classification,
            args = args
        )
        task_id = self.task_service.create_task(taskEntity)

        return task_id.id

