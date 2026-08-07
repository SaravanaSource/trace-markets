from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter

from app.core.logging import logger


class BaseJob(ABC):
    """
    Base class for executable jobs.

    Owns the execution lifecycle.
    """

    job_name = "unknown"

    

    def run(self):

        logger.info(
            "Starting {} job...",
            self.job_name,
        )

        start = perf_counter()

        try:

            self.execute()

            elapsed = perf_counter() - start

            logger.success(
                "{} completed in {:.3f} sec",
                self.job_name,
                elapsed,
            )

        except Exception as ex:

            logger.exception(ex)

            raise

    @abstractmethod
    def execute(self):
        """
        Child classes implement the job.
        """
