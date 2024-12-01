import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..service.stormtrooper import StormtrooperService

router = APIRouter(
    prefix='/classifier',
    tags=['classifier'],
    responses={404: {'description': 'Not found'}},
)


class ZeroShotRequest(BaseModel):
    """ """

    sentences: list[str]
    categories: list[str]


class FewShotRequest(BaseModel):
    """ """

    sample_sentences: list[str]
    sentences: list[str]
    categories: list[str]


# TODO zrobić docstring
SERVICES = {
    "stormtrooper": StormtrooperService()
}


@router.get('/zero_shot/{framework}', summary='Zero-shot', description='Returns a task id')
def zero_shot(framework: str, request: ZeroShotRequest):
    """This endpoint returns a JSON object with a greeting message.

    Example response:
    - **Hello**: A static string value "World"

    Useful for testing the API status.
    """
    # TODO: Logika która wybiera serwis na podstawie parametru framework
    # generuje id zadania, wrzuca zadanie do mongo i uruchamia zadanie
    task_id = uuid.uuid4()  # temp

    return {'taskId': task_id}


@router.get('/few_shot/{framework}', summary='Few-shot', description='Returns a task id')
def few_shot(framework: str, request: FewShotRequest):
    """This endpoint returns a JSON object with a task id.

    TODO: use request from body
    Example response:
    - Hello: 12345

    """
    service = SERVICES.get(framework)
    if not service:
        raise HTTPException(404, "framework not found")
    args = {
        "examples": {
            "text": [
                "ugotować ryż, dodać bazylię i oregano, na koniec posypać serem",
                "wymieszać sos a następnie polać nim potrawę",
                "obrać warzywa, pokroić i smażyć na oliwie z oliwek przez kilka minut",
                "Rafał Rafałczyk zdobył niecałe 20 procent głosów w swoim okręgu wyborczym",
                "partia Polska-Polska wywiązuje się ze swojej pierwszej obietnicy wyborczej",
                "Prezydent Szczecina przejechał gęś. Nie będzie mógł kontynuować swojej kadencji.",
                "Reakcja chemiczna - każdy proces, w wyniku którego pierwotna substancja zwana substratem przemienia się w inną substancję zwaną produktem.",
                "Energia potencjalna - energia, jaką ma ciało w zależności od położenia ciała w przestrzeni",
                "Kryptoanaliza (analiza kryptograficzna) - analiza systemu kryptograficznego w celu uzyskania informacji wrażliwej."
            ],
            "label": ["gotowanie", "gotowanie", "gotowanie", "polityka", "polityka", "polityka", "nauka", "nauka", "nauka"]
        },
        "text": "ugotować ryż, dodać bazylię i oregano, na koniec posypać serem"
    }
    task_id = service.add_few_shot(args=args)

    return {'taskId': '3'}


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
