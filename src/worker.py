import celery.app.log as log
from datetime import datetime
import os
import time

from celery import Celery, current_task

from .entity.task import *
from .repository.redis.task import TaskRepository
from .service.stormtrooper import StormtrooperService


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
logging = log.Logging(celery)
logger = logging.get_default_logger()
logger.setLevel(20) # INFO

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
    logger.info('start task...')

    # execute the task
    match taskEntity.framework:
        case Framework.STORMTROOPER:
            logger.info("framework: stormtrooper")
            result = stormtrooperService._few_shot_classification(taskEntity.args)
            # TODO: TASK IS NOT UPDATED AND DOESN'T SEEM TO CONCLUDE
            # TODO: save the actual result in TaskEntity
            taskEntity.result = TaskResult.SUCCEED
        case _:
            # other frameworks: not implemented
            logger.info(f"{taskEntity.framework} != {Framework.STORMTROOPER}")
            result = taskEntity.result = TaskResult.FAILED

    time.sleep(30)
    logger.info('end task')


    return result
