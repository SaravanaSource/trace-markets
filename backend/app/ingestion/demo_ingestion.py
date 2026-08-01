from app.core.logging import logger
from app.ingestion.base_ingestion import BaseIngestion
from app.storage.bronze_storage import BronzeStorage


class DemoIngestion(BaseIngestion):

    def __init__(self):
        self.storage = BronzeStorage()
     
    def fetch(self):
        logger.info("Fetching demo market data...")
        data = {
            "source": "demo",
            "market": "Indian Stock Market",
            "timestamp": "2026-08-01T10:45:00",
            "stocks": [
                {
                    "symbol": "INFY",
                    "price": 1645.50
                },
                {
                    "symbol": "TCS",
                    "price": 4215.80
                }
            ]
        }

        self.storage.save(
            source = 'demo',
            data = data
        )

        return data
