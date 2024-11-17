# 

from stormtrooper.set_fit import SetFitClassifier
from stormtrooper import ZeroShotClassifier
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from repository.task import *


class StormtrooperService:

    # register database
    async def create_task(self, task_id: str):
        """Tworzy nowe zadanie w bazie danych z domyślnym statusem PENDING."""
        await self.tasks_collection.insert_one({
            "task_id": task_id,
            "status": TaskStatus.PENDING.value,
        })

    async def update_task_status(self, task_id: str, status: TaskStatus):
        """Aktualizuje status zadania w bazie danych."""
        await self.tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": {"status": status.value}}
        )

    # anync zero-shot
    async def zero_shot_classification()

    # anync few-shot
    async def few_shot_classification()
    
