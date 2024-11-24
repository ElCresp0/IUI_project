from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from ...entity.task import TaskEntity


class TaskRepository:
    def __init__(self):
        MONGO_DETAILS = 'mongodb://my_mongo:27017'
        self.client = AsyncIOMotorClient(MONGO_DETAILS)
        self.db = self.client.taskdb
        self.task_collection = self.db.tas

    async def create_task(self, task: TaskEntity) -> str:
        task_dict = task.__dict__.copy()
        task_dict.pop('id', None)
        result = await self.task_collection.insert_one(task_dict)
        return str(result.inserted_id)

    async def update_task(self, task_id: str, task: TaskEntity) -> bool:
        existing_task = await self.task_collection.find_one({'_id': ObjectId(task_id)})
        if not existing_task:
            raise Exception('Task not found')

        task_dict = task.__dict__.copy()
        task_dict.pop('id', None)
        update_result = await self.task_collection.update_one({'_id': ObjectId(task_id)}, {'$set': task_dict})
        return update_result.modified_count != 0

    async def get_task(self, task_id: str) -> TaskEntity | None:
        task = await self.task_collection.find_one({'_id': ObjectId(task_id)})
        if not task:
            return None
        task['id'] = str(task['_id'])
        del task['_id']
        return TaskEntity(**task)

    async def remove_task(self, task_id: str) -> bool:
        delete_result = await self.task_collection.delete_one({'_id': ObjectId(task_id)})
        return delete_result.deleted_count != 0
