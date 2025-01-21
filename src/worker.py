import os
import threading
import time

import celery.app.log as log
from celery import Celery, current_task
from tqdm import tqdm

from .entity.task import Framework, Language, TaskEntity, TaskMode, TaskResult
from .repository.redis.task import TaskRepository
from .service.bielik_api import BielikApiService
from .service.model import ModelService
from .service.stormtrooper import StormtrooperService

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')
logging = log.Logging(celery)
logger = logging.get_default_logger()
logger.setLevel(20)  # INFO

task_repository = TaskRepository()


@celery.task(name='create_task')
def create_task(taskEntityDict: dict):
    """Executes a task based on the taskEntity

    updates the task in redis

    IN: JSON serialized taskEntity

    """
    taskEntity = TaskEntity(**taskEntityDict)
    path = str
    logger.info(list(tqdm._instances))
    task_id = current_task.request.id
    task_repository.update_task_progress(task_id, '0%')
    stop_monitoring = False
    logger.info(f'start task {task_id} ...')

    def monitor_library_progress():
        nonlocal stop_monitoring
        nonlocal task_id
        nonlocal taskEntity
        while (
            taskEntity.framework == Framework.STORMTROOPER or taskEntity.framework == Framework.BIELIK_API
        ) and not stop_monitoring:
            active_bars = list(tqdm._instances)
            for bar in active_bars:
                if bar.total:
                    progress_percent = (bar.n / bar.total) * 100
                    task_repository.update_task_progress(
                        task_id, f'{progress_percent:.2f}%')
                else:
                    task_repository.update_task_progress(
                        task_id, 'Started, but progress bar not supported')
            time.sleep(2)

    monitor_thread = threading.Thread(
        target=monitor_library_progress, daemon=True)
    monitor_thread.start()

    match taskEntity.language:
        case Language.PL:
            if taskEntity.framework == Framework.BIELIK_API:
                path = ''
            elif taskEntity.mode == TaskMode.FEW_SHOT or taskEntity.mode == TaskMode.ZERO_SHOT:
                path = ModelService().get_sbert_base_cased_pl()
            else:
                logger.info(f'{taskEntity.framework}: unknown mode')
                result = taskEntity.result = TaskResult.FAILED
        case Language.EN:
            if taskEntity.mode == TaskMode.FEW_SHOT:
                path = ModelService().get_few_shot_fb_bart_large_mnli()
            elif taskEntity.mode == TaskMode.ZERO_SHOT:
                path = ModelService().get_bart_large_mnli()
            else:
                logger.info(f'{taskEntity.framework}: unknown mode')
                result = taskEntity.result = TaskResult.FAILED
        case _:
            logger.info(
                f'{taskEntity.language} is not {Language.PL} and not {Language.EN}')
            result = taskEntity.result = TaskResult.FAILED

    # execute the task
    match taskEntity.framework:
        case Framework.STORMTROOPER:
            logger.info('framework: stormtrooper')
            stormtrooperService = StormtrooperService(path)
            if taskEntity.mode == TaskMode.FEW_SHOT:
                logger.info('started few shot')
                result = stormtrooperService.few_shot_classification(
                    taskEntity.args)
                taskEntity.result = TaskResult.SUCCEED  # to chyba można usunac
            elif taskEntity.mode == TaskMode.ZERO_SHOT:
                logger.info('started zero shot')
                result = stormtrooperService.zero_shot_classification(
                    taskEntity.args)
                taskEntity.result = TaskResult.SUCCEED  # to chyba można usunac
            else:
                logger.info(f'{taskEntity.framework}: unknown mode')
                result = taskEntity.result = TaskResult.FAILED
        case Framework.BIELIK_API:
            bielikApiService = BielikApiService()
            if taskEntity.mode == TaskMode.FEW_SHOT:
                logger.info('started few shot')
                result = bielikApiService.few_shot_classification(
                    taskEntity.args)
                taskEntity.result = TaskResult.SUCCEED  # to chyba można usunac
            elif taskEntity.mode == TaskMode.ZERO_SHOT:
                logger.info('started zero shot')
                result = bielikApiService.zero_shot_classification(
                    taskEntity.args)
                taskEntity.result = TaskResult.SUCCEED  # to chyba można usunac
            else:
                logger.info(f'{taskEntity.framework}: unknown mode')
                result = taskEntity.result = TaskResult.FAILED
        case _:
            logger.info(f'{taskEntity.framework}: not supported framework')
            result = taskEntity.result = TaskResult.FAILED

    logger.info('end task')
    stop_monitoring = True
    monitor_thread.join()

    task_repository.update_task_progress(task_id, '100%')
    return result
