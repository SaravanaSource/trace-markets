from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from app.core.logging import logger
from app.models.stock_record import StockRecord


class SilverStorage:
    """
    Stores canonical StockRecord objects.

    Silver data is standardized and cleaned.
    """

    def __init__(self):

        self.base_path = Path("data/silver")

    def save(
        self,
        record: StockRecord,
    ) -> Path:

        today = datetime.now(UTC)

        folder = (
            self.base_path
            / f"exchange={record.exchange}"
            / f"year={today:%Y}"
            / f"month={today:%m}"
            / f"day={today:%d}"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        files = list(folder.glob("part-*.json"))

        next_number = len(files) + 1

        path = folder / f"part-{next_number:06}.json"

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(record),
                file,
                indent=4,
                default=str,
            )

        logger.success(
            "Silver file written -> {}",
            path,
        )

        return path
