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

    def _zero_shot_classification(self, args: dict):
        pass
        # TODO here add logic for stormtrooper

        # TODO here we can add some additional notification
        # https://fastapi.tiangolo.com/tutorial/background-tasks/


    def _few_shot_classification(self, args: dict):
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

    def add_zero_shot(self) -> TaskEntity:
        pass

    def add_few_shot(self, args) -> TaskEntity:
        pass