from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any

from app.core.logging import logger
from app.storage.bronze_storage import BronzeStorage


### Template method design pattern ###

class BaseIngestion(ABC):
    """
    Base class for every ingestion job.

    Owns the ingestion lifecycle.

    Child classes only implement fetch().
    """

    source : str = "unknown"

    def __init__(self):
        self.storage = BronzeStorage()

    def run(self):
        logger.info(f"Starting {self.source} ingestion job")
        start = perf_counter()

        try:

            data = self.fetch()
            self.validate(data)

            path = self.storage.save(
                source = self.source,
                data = data
            )

            elapsed = perf_counter() - start
            logger.success(f" {self.source}  Ingestion completed in {elapsed:.3f} sec" )
            return path

        except Exception as exe:
            logger.exception(exe)
            raise

    @abstractmethod
    def fetch(self) -> Any:
        """
        child class must implement
        """

    def validate(self, data:Any):

        if data is None:
            raise ValueError("No data returned from fetch().")

