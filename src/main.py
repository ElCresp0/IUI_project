from fastapi import FastAPI

from .routers import (
    classifier,  # TODO kropka jakby co
    task,
)

app = FastAPI(
    title='renameme',
    description='Fill the description',
    version='0.1',
)

app.include_router(classifier.router)
app.include_router(task.router)
