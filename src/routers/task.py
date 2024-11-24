from fastapi import APIRouter, HTTPException

from ..entity.task import TaskResult
from ..service.task import TaskService

router = APIRouter(
    prefix='/task',
    tags=['task'],
    responses={404: {'description': 'Not found'}},
)

# TODO change to dependency injection
task_service = TaskService()


@router.get('/status/{task_id}', summary='Task status', description='Returns a task status')
async def status(task_id: str):
    """Endpoint to fetch the status of a task."""
    try:
        status = await task_service.get_task_status(task_id)
        return {'taskId': task_id, 'status': status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/result/{task_id}', summary='Task result', description='Returns a task result')
async def result(task_id: str):
    """Endpoint to fetch the result of a task."""
    try:
        result = await task_service.get_task_result(task_id)
        return {'taskId': task_id, 'result': result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


#######################
# ENDPOINTS FOR TESTING#
#######################
@router.post('/test_create', summary='Create task', description='Creates a new task')
async def create_task():
    """Endpoint to create a new task."""
    try:
        task_type=2
        task_id = await task_service.create_task(task_type)
        return {'taskId': task_id, 'message': 'Task created successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/test_get/{task_id}', summary='Get task', description='Get task')
async def get_task(task_id: str):
    """Get task."""
    try:
        task = await task_service.get_task(task_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



