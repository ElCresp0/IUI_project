from celery.result import AsyncResult

#TODO użyyć klase TaskEntity i  zwracać więcej informacji
class TaskRepository:
    def get_task(self, task_id: str) -> dict | None:
        task_result = AsyncResult(task_id)
        if(task_result):
            return {'task_id': task_id, 'status': task_result.status, 'result': task_result.result}
        else:
            None
    
    
