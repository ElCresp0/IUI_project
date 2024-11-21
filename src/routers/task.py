from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix='/task',
    tags=['task'],
    responses={404: {'description': 'Not found'}},
)


#TODO zrobić docstring

@router.get('/status/{task_id}', summary='Task status', description='Returns a task status')
def status(task_id: str):
    """This endpoint returns a JSON object with a greeting message.

    Example response:
    - **Hello**: A static string value "World"

    Useful for testing the API status.
    """

    # TODO: użyć task service, wywołać jakieś operacje na mongo, pobrać dane, zwrócić status
    status = "STATUS ZADANIA"

    return {'taskId': status}

@router.get('/result/{task_id}', summary='Task result', description='Returns a task result')
def result(task_id: str):
    """This endpoint returns a JSON object with a task id.

    Example response:
    - Hello: 12345

    """
    # TODO: 
    result = "WYBRANA KLASA"

    return {'result': result}
