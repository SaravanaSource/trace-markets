from app.core.logging import logger

### Template method design pattern ###

class BaseIngestion:
    def run(self):
        logger.info("Starting ingestion job")

        self.fetch()

        logger.success("Ingestion completed")

    def fetch(self):
        raise NotImplementedError
