from __future__ import annotations

from app.jobs.base_job import BaseJob
from app.ingestion.api_ingestion import APIIngestion


class BronzeJob(BaseJob):
    """
    Executes Bronze ingestion jobs.
    """

    job_name = "Bronze"

    def __init__(self):
        self.ingestion = APIIngestion()

    def execute(self):
        self.ingestion.run()
