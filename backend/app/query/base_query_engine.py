from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseQueryEngine(ABC):
    """
    Contract for analytical query engines.
    """

    @abstractmethod
    def query(
        self,
        sql: str,
    ) -> Any:
        """
        Execute an analytical SQL query.
        """
