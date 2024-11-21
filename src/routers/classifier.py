from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix='/classifier',
    tags=['classifier'],
    responses={404: {'description': 'Not found'}},
)

class ZeroShotRequest(BaseModel):
    """
    
    """
    sentences: list[str]
    categories: list[str]

class FewShotRequest(BaseModel):
    """
    
    """
    sample_sentences: list[str]
    sentences: list[str]
    categories: list[str]

#TODO zrobić docstring

@router.get('/zero_shot/{framework}', summary='Zero-shot', description='Returns a task id')
def zero_shot(framework: str, request: ZeroShotRequest):
    """This endpoint returns a JSON object with a greeting message.

    Example response:
    - **Hello**: A static string value "World"

    Useful for testing the API status.
    """

    # TODO: Logika która wybiera serwis na podstawie parametru framework
    # generuje id zadania, wrzuca zadanie do mongo i uruchamia zadanie
    task_id = uuid.uuid4() #temp

    return {'taskId': task_id}

@router.get('/few_shot/{framework}', summary='Few-shot', description='Returns a task id')
def few_shot(framework: str, request: FewShotRequest):
    """This endpoint returns a JSON object with a task id.

    Example response:
    - Hello: 12345

    """
    # TODO: Logika która wybiera serwis na podstawie parametru framework
    # generuje id zadania, wrzuca zadanie do mongo i uruchamia zadanie
    task_id = uuid.uuid4() #temp
    
    return {'taskId': task_id}


# @router.put(
#     '/',
#     summary='Greet by Name',
#     description='Returns a greeting message with the provided name.',
#     response_model=HelloResponse,
# )
# def hello_name(name: str):
#     """Greet the user by their name.

#     This endpoint accepts a query parameter `name` and returns a JSON object with a greeting message.

#     - **name**: The name of the person to greet.

#     Example response:
#     - **Hello**: The name provided in the input.
#     """
#     return {'Hello': name}
