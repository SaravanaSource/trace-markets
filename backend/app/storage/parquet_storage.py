from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from app.storage.base_storage import BaseStorage


class ParquetStorage(BaseStorage):
    """
    Parquet implementation of the storage contract.

    Intended for tabular analytical data.
    """

    def save(
        self,
        data: Any,
        path: Path,
    ) -> Path:
        """
        Persist tabular data as a Parquet file.
        """

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        rows = self._normalize(data)

        table = pa.Table.from_pylist(rows)

        pq.write_table(
            table,
            path,
        )

        return path

    def load(
        self,
        path: Path,
    ) -> list[dict[str, Any]]:
        """
        Load a Parquet file into a list of dictionaries.
        """

        table = pq.read_table(path)

        return table.to_pylist()

    @staticmethod
    def _normalize(
        data: Any,
    ) -> list[dict[str, Any]]:
        """
        Convert supported input objects into rows.
        """

        if is_dataclass(data):
            return [asdict(data)]

        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            rows = []

            for item in data:
                if is_dataclass(item):
                    rows.append(asdict(item))
                elif isinstance(item, dict):
                    rows.append(item)
                else:
                    raise TypeError(
                        "ParquetStorage expects dictionaries "
                        "or dataclass instances."
                    )

            return rows

        raise TypeError(
            "ParquetStorage expects a dictionary, "
            "dataclass, or list of dictionaries/dataclasses."
        )
