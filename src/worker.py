import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

#TODO dodać jakiś sposób aby przyjmował zadanie od frameworków - może przekazywanie funkcji ?
@celery.task(name='create_task')
def create_task(task_type):
    print('start task...')
    time.sleep(int(task_type) * 10)
    print('end task')
    return True
