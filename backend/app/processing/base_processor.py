from __future__ import annotations

from abc import ABC, abstractmethod

from app.storage.bronze_record import BronzeRecord


class BaseProcessor(ABC):
    """
    Base class for all processing stages.

    A processor transforms one model into another.
    """

    @abstractmethod
    def process(self, record: BronzeRecord):
        """
        Transform a BronzeRecord into another model.
        """
