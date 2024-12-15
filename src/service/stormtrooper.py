import logging

from stormtrooper.set_fit import SetFitClassifier
from stormtrooper import ZeroShotClassifier
from stormtrooper import Trooper

# from ..entity.task import TaskMode, TaskStatus, TaskEntity
from .framework import Framework
from .model import ModelService

class StormtrooperService(Framework):
    def __init__(self):
        super().__init__()
        logging.info("loading the model")
        self.model_path = ModelService().get_sbert_base_cased_pl()
        self.few_shot_model = SetFitClassifier(self.model_path) # SetFitClassifier
        self.zero_shot_model = Trooper(self.model_path) # ZeroShotClassifier ?
