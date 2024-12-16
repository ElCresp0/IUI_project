import logging

from stormtrooper import Trooper
from .framework import Framework

class StormtrooperService(Framework):
    def __init__(self, path: str):
        super().__init__()
        logging.info("loading the model")         
        self.model = Trooper(path)
