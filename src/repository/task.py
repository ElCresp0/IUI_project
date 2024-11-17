from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from entity import TaskEntity, TaskStatus
from datetime import datetime

class TaskRepository:

    def __init__(self):
        MONGO_DETAILS = "mongodb://localhost:27017"
        self.client = AsyncIOMotorClient(MONGO_DETAILS)
        self.db = self.client.taskdb
        self.task_collection = self.db.tas

    async def create_task(self) -> str:
        task_dict = {
        "status" :  TaskStatus.COMPLETED.value}
        result = await self.task_collection.insert_one(task_dict)
        return str(result.inserted_id)

    async def start_task(self, task_id: str):
        task = await self.task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise Exception("Task not found")

        if task.get("status") != TaskStatus.PENDING.value:
            raise Exception("Task is not in a startable state")

        update_result = await self.task_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": TaskStatus.IN_PROGRESS.value, "start_time": datetime.now()}}
        )
        if update_result.modified_count == 0:
            raise Exception("Failed to update task status")

    async def finish_task(self, task_id: str):
        task = await self.task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise Exception("Task not found")

        if task.get("status") != TaskStatus.IN_PROGRESS.value:
            raise Exception("Task is not in a finishable state")

        update_result = await self.task_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": TaskStatus.COMPLETED.value, "end_time": datetime.now()}}
        )
        if update_result.modified_count == 0:
            raise Exception("Failed to update task status")

    async def get_task(self, task_id: str) -> TaskEntity:
        task = await self.task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise Exception("Task not found")
        task["id"] = str(task["_id"])
        del task["_id"]
        return TaskEntity(**task)
    
    async def remove_task(self, task_id: str):
        task = await self.task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise Exception("Task not found")

        delete_result = await self.task_collection.delete_one({"_id": ObjectId(task_id)})
        if delete_result.deleted_count == 0:
            raise Exception("Failed to delete task")