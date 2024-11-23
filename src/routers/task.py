from fastapi import APIRouter, HTTPException
from entity.task import TaskResult
from pydantic import BaseModel
from service.task import TaskService
import uuid

router = APIRouter(
    prefix='/task',
    tags=['task'],
    responses={404: {'description': 'Not found'}},
)

#TODO change to dependency injection
task_service = TaskService()

@router.get('/status/{task_id}', summary='Task status', description='Returns a task status')
async def status(task_id: str):
    """
    Endpoint to fetch the status of a task.
    """
    try:
        status = await task_service.get_task_status(task_id)
        return {'taskId': task_id, 'status': status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/result/{task_id}', summary='Task result', description='Returns a task result')
async def result(task_id: str):
    """
    Endpoint to fetch the result of a task.
    """
    try:
        result = await task_service.get_task_result(task_id)
        return {'taskId': task_id, 'result': result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


#######################
#ENDPOINTS FOR TESTING#
#######################
@router.post('/create', summary='Create task', description='Creates a new task')
async def create_task():
    """
    Endpoint to create a new task.
    """
    try:
        task_id = await task_service.create_task()
        return {'taskId': task_id, 'message': 'Task created successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/delete/{task_id}', summary='Delete task', description='Deletes a task')
async def delete_task(task_id: str):
    """
    Endpoint to delete a task.
    """
    try:
        await task_service.delete_task(task_id)
        return {'taskId': task_id, 'message': 'Task deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/start/{task_id}', summary='Start task', description='Starts a task')
async def start_task(task_id: str):
    """
    Endpoint to start a task.
    """
    try:
        await task_service.start_task(task_id)
        return {'taskId': task_id, 'message': 'Task started successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/finish/{task_id}', summary='Finish task', description='Finishes a task')
async def finish_task(task_id: str, result: TaskResult):
    """
    Endpoint to finish a task and set its result.
    """
    try:
        await task_service.finish_task(task_id, result)
        return {'taskId': task_id, 'message': 'Task finished successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

