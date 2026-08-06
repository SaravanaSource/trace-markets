from __future__ import annotations

from app.core.logging import logger
from app.processing.silver_processor import SilverProcessor
from app.storage.bronze_record import BronzeRecord
from app.storage.silver_storage import SilverStorage


class ProcessingPipeline:
    """
    Executes post-ingestion processing stages.

    Current stages:

        Bronze
            ↓
        Silver

    Future:

        Bronze
            ↓
        Silver
            ↓
        Gold
            ↓
        Feature Engineering
            ↓
        AI
    """

    def __init__(self):

        self.silver_processor = SilverProcessor()
        self.silver_storage = SilverStorage()

    def run(
        self,
        bronze_record: BronzeRecord,
    ):

        logger.info("Starting processing pipeline...")

        silver_record = self.silver_processor.process(
            bronze_record
        )

        self.silver_storage.save(
            silver_record
        )

        logger.success(
            "Processing pipeline completed."
        )
