from app.core.logging import logger
from app.ingestion.base_ingestion import BaseIngestion


class DemoIngestion(BaseIngestion):

    source = "demo"

    def fetch(self):

        logger.info("Fetching demo market data...")
        
        return  {
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
