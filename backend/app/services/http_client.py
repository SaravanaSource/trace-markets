from __future__ import annotations
from typing import Any
import httpx
import time
from datetime import datetime, UTC

from app.core.config import settings
from app.core.logging import logger
from app.models.bronze_record import BronzeRecord
from app.core.exceptions import  InvalidResponseError, RetryLimitExceededError

class HttpClient:
    """
    Generic HTTP client for Trace Markets.
    """

    def __init__(self):
        self.timeout = settings.HTTP_TIMEOUT
        self.max_retries = settings.HTTP_MAX_RETRIES
        self.retry_delays = settings.HTTP_RETRY_DELAY


    def get(self, url:str) -> Any:

        last_exception = None

        for attempt in range(1, self.max_retries +1):

            logger.info(f"Attempt {attempt}/{self.max_retries} sending GET request -> {url}")

            try:
                with httpx.Client(timeout = self.timeout) as client:
                    response =client.get(url)
                    response.raise_for_status()
                    logger.success(f"Received HTTP {response.status_code}")

                    metadata = {
                        "source": "api",
                        "url" : url,
                        "http_status" : response.status_code,
                        "fetched_at" : datetime.now(UTC).isoformat()
                    }

                    try:

                        return BronzeRecord(
                            metadata= metadata,
                            payload= response.json()
                        )
                    
                    except ValueError as exc:
                        raise InvalidResponseError (
                            "Response is not valid json"
                        ) from exc
                    
            except httpx.HTTPError as exc:

                last_exception = exc
                logger.warning(f"Attempt {attempt} failed: {exc}")

                if attempt < self.max_retries:
                    wait = self.retry_delays * (2 ** (attempt-1)) # Exponential back off
                    logger.info(f"retrying in {wait} seconds ...")
                    time.sleep(wait)

        raise RetryLimitExceededError (
            f"failed after {self.max_retries} attempts"
        ) from last_exception