from abc import ABC, abstractmethod
from typing import Any


class Framework(ABC):
    """Base class for text-classification frameworks:

    - Stormtrooper
    - Bielik_Api
    """

    def __init__(self):
        self.model: Any

    @abstractmethod
    def zero_shot_classification(self, args: dict):
        """Abstract method to perform zero-shot text classification.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def few_shot_classification(self, args: dict):
        """Abstract method to perform few-shot text classification.

        Must be implemented by subclasses.
        """
        pass
