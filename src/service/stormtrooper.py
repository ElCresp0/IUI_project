from stormtrooper.set_fit import SetFitClassifier
from stormtrooper import ZeroShotClassifier
from repository.task import *
from fastapi import BackgroundTasks

def _zero_shot_classification(path_model, user_option, id):
    repository = TaskRepository()
    repository.start_task(id)
    
    # TODO here add logic for stormtrooper
    
    repository.finish_task(id)
    
    # TODO here we can add some additional notification
    # https://fastapi.tiangolo.com/tutorial/background-tasks/

def _few_shot_classification():
    pass

class StormtrooperService:
    
    def __init__(self):
        self.repository = TaskRepository()
        

    def add_zero_shot(self, path_model, user_option, background_tasks: BackgroundTasks):
        id = self.repository.create_task()
        
        background_tasks.add_task(_zero_shot_classification, path_model, user_option, id)
        
        return id
    

    
