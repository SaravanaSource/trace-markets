from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class StockRecord:
    """
    Canonical stock model used by the Silver layer.

    Every connector transforms its raw payload into
    this business model.
    """

    symbol: str
    company_name: str

    exchange: str
    country: str
    currency: str

    sector: str
    industry: str

    asset_type: str

    price: float

    previous_close: float | None

    open: float | None
    high: float | None
    low: float | None

    volume: int | None

    market_cap: float | None

    timestamp: datetime

    source: str

    ingested_at: datetime
