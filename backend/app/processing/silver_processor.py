from __future__ import annotations

from datetime import UTC, datetime

from app.processing.base_processor import BaseProcessor
from app.models.stock_record import StockRecord
from app.models.bronze_record import BronzeRecord


class SilverProcessor(BaseProcessor):
    """
    Converts Bronze records into the canonical
    StockRecord model.
    """

    def process(
        self,
        record: BronzeRecord,
    ) -> StockRecord:

        payload = record.payload

        return StockRecord(
            symbol=str(payload["id"]),
            company_name=payload["title"],
            exchange="UNKNOWN",
            country="UNKNOWN",
            currency="UNKNOWN",
            sector="UNKNOWN",
            industry="UNKNOWN",
            asset_type="UNKNOWN",
            price=0.0,
            previous_close=None,
            open=None,
            high=None,
            low=None,
            volume=None,
            market_cap=None,
            timestamp=datetime.now(UTC),
            source=record.metadata["source"],
            ingested_at=datetime.now(UTC),
        )
