from datetime import datetime
import os
import time

from celery import Celery

from .entity.task import TaskEntity, TaskStatus
from .repository.redis.task import TaskRepository

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

task_repository = TaskRepository()

#TODO dodać jakiś sposób aby przyjmował zadanie od frameworków - może przekazywanie funkcji ?
@celery.task(name='create_task')
def create_task(taskEntity: TaskEntity):
    """
    executes a task based on the (callable, args) duo
    updates the task in redis

    IN: taskEntity

    """
    # TODO: print -> logging
    print('start task...')
    taskEntity.start_time=datetime.now()
    taskEntity.status = TaskStatus.IN_PROGRESS
    task_repository.update_task(taskEntity)

    # execute the task
    taskEntity.result = taskEntity.callable(taskEntity.args)

    time.sleep(300)
    print('end task')
    taskEntity.status = TaskStatus.COMPLETED
    taskEntity.end_time = datetime.now()
    task_repository.update_task(taskEntity)

    return True
