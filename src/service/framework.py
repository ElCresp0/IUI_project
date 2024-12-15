import logging
from typing import Any

import pandas as pd
from ..entity.task import TaskEntity
import numpy as np
# from ..service.task import TaskService


class Framework:
    """
    Base class for text-classification frameworks:
    - Stormtrooper
    - Bullet
    - TARS
    """

    def __init__(self):
        self.few_shot_model : Any
        self.zero_shot_model : Any

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

        self.zero_shot_model.fit(None, label)

        df = pd.DataFrame({
            "text": text
        })
        logging.warning("test data:\n%s", df)
        y_pred = self.zero_shot_model.predict(df["text"])

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
        self.few_shot_model.fit(training_data["text"], training_data["label"])

        df = pd.DataFrame({
            "text": text
        })
        logging.warning("test data:\n%s", df)
        y_pred = self.few_shot_model.predict(df["text"])

        logging.warning(f"framework y_pred: {y_pred}")
    
        return y_pred.tolist()