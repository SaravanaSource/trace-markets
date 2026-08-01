from __future__ import annotations
from typing import Any
import httpx

from app.core.logging import logger

class HttpClient:
    """
    Generic HTTP client for Trace Markets.
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def get(self, url:str) -> Any:

        logger.info(f"sending GET request -> {url}")
        with httpx.Client(timeout = self.timeout) as client:
            response =client.get(url)
            response.raise_for_status()
            logger.success(f"Received HTTP {response.status_code}")
            return response.json()