from abc import ABC, abstractmethod


class BaseRule(ABC):
    """
    Base class for all Data Quality rules.
    """

    @abstractmethod
    def validate(self, data: dict):
        """
        Validate a record.
        """
        pass