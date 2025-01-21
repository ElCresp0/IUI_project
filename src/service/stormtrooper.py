import logging

import pandas as pd
import torch
from billiard.process import current_process
from stormtrooper import Trooper

from .framework import Framework


class StormtrooperService(Framework):
    """This class organizes stormtrooper framework tasks

    Use it to execute zero_shot and few_shot text classification
    """

    def __init__(self, path: str):
        super().__init__()
        logging.info('loading the model')
        worker_index = current_process().index
        if torch.cuda.is_available() and torch.cuda.device_count() > worker_index:
            self.model = Trooper(path, device='cuda:' + str(worker_index))
        else:
            self.model = Trooper(path, device='cpu')

    def zero_shot_classification(self, args: dict):
        """Performs zero shot text classification

        should be called as a BackGround task

        In:
        - labels:   user defined labels for classification
        - text:     text to be classified

        Out:
        - model predictions
        """
        label: dict = args['label']
        text: list = args['text']

        self.model.fit(None, label)

        df = pd.DataFrame({'text': text})
        logging.warning('test data:\n%s', df)
        y_pred = self.model.predict(df['text'])

        logging.warning(f'framework y_pred: {y_pred}')

        return y_pred.tolist()

    def few_shot_classification(self, args: dict):
        """Performs few shot text classification

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

        examples: dict = args['examples']
        text: list = args['text']

        training_data = pd.DataFrame(
            {'text': examples['text'], 'label': examples['label']})
        logging.warning('Training data:\n%s', training_data)
        self.model.fit(training_data['text'], training_data['label'])

        df = pd.DataFrame({'text': text})
        logging.warning('test data:\n%s', df)
        y_pred = self.model.predict(df['text'])

        logging.warning(f'framework y_pred: {y_pred}')

        return y_pred.tolist()
