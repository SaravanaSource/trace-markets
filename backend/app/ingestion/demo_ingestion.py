from app.core.logging import logger
from app.ingestion.base_ingestion import BaseIngestion


class DemoIngestion(BaseIngestion):
    def fetch(self):
        logger.info("Fetching demo market data...")
