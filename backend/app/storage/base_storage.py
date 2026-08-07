from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseStorage(ABC):
    """
    Base interface for all storage engines.

    A storage engine is responsible only for
    persisting and loading data.

    Examples
    --------
    - JSON
    - Parquet
    - Iceberg
    - Delta Lake
    """

    @abstractmethod
    def save(
        self,
        data: Any,
        path: Path,
    ) -> Path:
        """
        Persist data to storage.

        Parameters
        ----------
        data
            Object to persist.

        path
            Destination file path.

        Returns
        -------
        Path
            Written file path.
        """

    @abstractmethod
    def load(
        self,
        path: Path,
    ) -> Any:
        """
        Load data from storage.
        """
