import logging

from stormtrooper import Trooper
from .framework import Framework
import pandas as pd
import numpy as np

class StormtrooperService(Framework):
    def __init__(self, path: str):
        super().__init__()
        logging.info("loading the model")         
        self.model = Trooper(path)

    def zero_shot_classification(self, args: dict):
        """
        performs zero shot text classification
        should be called as a BackGround task

        In:
        - labels:   user defined labels for classification
        - text:     text to be classified

        Out:
        - model predictions
        """
        
        label: dict = args["label"]
        text: list = args["text"]

        self.model.fit(None, label)

        df = pd.DataFrame({
            "text": text
        })
        logging.warning("test data:\n%s", df)
        y_pred = self.model.predict(df["text"])

        logging.warning(f"framework y_pred: {y_pred}")
            
        return y_pred.tolist()


    def few_shot_classification(self, args: dict):
        """
        performs few shot text classification
        should be called as a BackGround task

        In:
        - examples: list of tuples of (example_text, label)
        - labels:   user defined labels for classification
        - text:     text to be classified

        Out:
        - model predictions
        """

        # this is based on stormtrooper
        # if it differs in other frameworks, move it to subclasses

        examples: dict = args["examples"]
        text: list = args["text"]

        training_data = pd.DataFrame({
            "text": examples["text"],
            "label": examples["label"]
        })
        logging.warning("Training data:\n%s", training_data)
        self.model.fit(training_data["text"], training_data["label"])

        df = pd.DataFrame({
            "text": text
        })
        logging.warning("test data:\n%s", df)
        y_pred = self.model.predict(df["text"])

        logging.warning(f"framework y_pred: {y_pred}")
    
        return y_pred.tolist()