from datetime import datetime
import logging
import os
import time

from celery import Celery, current_task

from .entity.task import *
from .repository.redis.task import TaskRepository
from .service.stormtrooper import StormtrooperService


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

task_repository = TaskRepository()
stormtrooperService = StormtrooperService()

@celery.task(name='create_task')
def create_task(taskEntityDict: dict):
    """
    executes a task based on the taskEntity
    updates the task in redis

    IN: JSON serialized taskEntity

    """

    taskEntity = TaskEntity(**taskEntityDict)
    # TODO: print -> logging
    logging.info('start task...')
    taskEntity.id = str(current_task.request.id)
    taskEntity.start_time = datetime.now().strftime(DATEFORMAT)
    taskEntity.status = TaskStatus.IN_PROGRESS
    task_repository.update_task(taskEntity)

    # execute the task
    match taskEntity.framework:
        case Framework.STORMTROOPER:
            result = stormtrooperService._few_shot_classification(taskEntity.args)
            # TODO: TASK IS NOT UPDATED AND DOESN'T SEEM TO CONCLUDE
            # TODO: save the actual result in TaskEntity
            taskEntity.result = TaskResult.SUCCEED
        case _:
            taskEntity.result = TaskResult.FAILED

    time.sleep(300)
    print('end task')
    taskEntity.status = TaskStatus.COMPLETED
    taskEntity.end_time = datetime.now()
    task_repository.update_task(taskEntity)

    return True
