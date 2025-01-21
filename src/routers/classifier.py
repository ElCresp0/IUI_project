import logging

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from ..entity.task import TaskEntity, TaskMode, TaskStatus, map_to_enum
from ..service.task import TaskService

router = APIRouter(
    prefix='/classifier',
    tags=['classifier'],
    responses={404: {'description': 'Not found'}},
)


class ZeroShotRequest(BaseModel):
    """Class representation on a zero_shot request.

    It consists of unlabelled sentences and categories.
    """

    sentences: list[str]
    categories: list[str]


class FewShotRequest(BaseModel):
    """Class representation on a few_shot request.

    It consists of sample sentences, unlabelled sentences and categories.
    """

    sample_sentences: list[str]
    sentences: list[str]
    categories: list[str]


taskService = TaskService()


@router.post('/zero_shot/{framework}', summary='Zero-shot', description='Returns a task id')
async def zero_shot(
    framework: str = 'bielik_api',
    language: str = 'pl',
    request: ZeroShotRequest | None = None,
):
    """This endpoint returns a JSON object with a greeting message.

    Example response:
    - **Hello**: A static string value "World"

    Useful for testing the API status.
    """
    if not request:
        request = Body(
            ...,
            example={
                'sentences': [
                    'Ugotować ryż, dodać bazylię i oregano, na koniec posypać serem.',
                    'Reakcja chemiczna - proces przemiany substancji.',
                    'Prezydent Szczecina przejechał gęś.',
                    'Partia polityczna ogłasza nowe reformy edukacyjne.',
                ],
                'categories': ['gotowanie', 'polityka', 'nauka'],
            },
        )
    try:
        mapped_language, mapped_framework = map_to_enum(language, framework)
        args = {'label': request.categories, 'text': request.sentences}

        # TODO: rodzaj modelu powinien być zależny od wybranego języka, tylko
        task = TaskEntity(
            id=None,
            start_time=None,
            end_time=None,
            mode=TaskMode.ZERO_SHOT,
            framework=mapped_framework,
            args=args,
            language=mapped_language,
            status=TaskStatus.PENDING,
            result=None,
        )
        task_id = await taskService.create_task(task)
        # TODO: global logging config and formatting
        logging.info(f'{__name__} :: task_id: {task_id}')
        return {'taskId': task_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post('/few_shot/{framework}', summary='Few-shot', description='Returns a task id')
async def few_shot(
    framework: str = 'bielik_api',
    language: str = 'pl',
    request: FewShotRequest | None = None,
):
    """This endpoint returns a JSON object with a task id.

    TODO: use request from body
    Example response:
    - Hello: 12345

    """
    if not request:
        request = Body(
            ...,
            example={
                'sample_sentences': [
                    'ugotować ryż, dodać bazylię i oregano, na koniec posypać serem',
                    'wymieszać sos a następnie polać nim potrawę',
                    'obrać warzywa, pokroić i smażyć na oliwie z oliwek przez kilka minut',
                    'Rafał Rafałczyk zdobył niecałe 20 procent głosów w swoim okręgu wyborczym',
                    'partia Polska-Polska wywiązuje się ze swojej pierwszej obietnicy wyborczej',
                    'Prezydent Szczecina przejechał gęś. Nie będzie mógł kontynuować swojej kadencji.',
                    'Reakcja chemiczna - każdy proces, w wyniku którego pierwotna substancja zwana '
                    'substratem przemienia się w inną substancję zwaną produktem.',
                    'Energia potencjalna - energia, jaką ma ciało w zależności od położenia ciała w przestrzeni',
                    'Kryptoanaliza (analiza kryptograficzna) - analiza systemu '
                    'kryptograficznego w celu uzyskania informacji wrażliwej.',
                ],
                'sentences': [
                    'ugotować ryż, dodać bazylię i oregano, na koniec posypać serem',
                    'Reakcja chemiczna - proces przemiany substancji.',
                    'Prezydent Szczecina przejechał gęś.',
                ],
                'categories': [
                    'gotowanie',
                    'gotowanie',
                    'gotowanie',
                    'polityka',
                    'polityka',
                    'polityka',
                    'nauka',
                    'nauka',
                    'nauka',
                ],
            },
        )
    try:
        mapped_language, mapped_framework = map_to_enum(language, framework)
        args = {
            'examples': {'text': request.sample_sentences, 'label': request.categories},
            'text': request.sentences,
        }
        task = TaskEntity(
            id=None,
            start_time=None,
            end_time=None,
            mode=TaskMode.FEW_SHOT,
            framework=mapped_framework,
            args=args,
            language=mapped_language,
            status=TaskStatus.PENDING,
            result=None,
        )
        task_id = await taskService.create_task(task)
        # TODO: global logging config and formatting
        logging.info(f'{__name__} :: task_id: {task_id}')
        return {'taskId': str(task_id)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
