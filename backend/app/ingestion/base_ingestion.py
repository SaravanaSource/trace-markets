from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from time import perf_counter
from typing import Any

from app.core.logging import logger
from app.schema.schema_diff import SchemaDiff
from app.schema.schema_registry import SchemaRegistry
from app.schema.schema_utils import SchemaUtils
from app.storage.bronze_storage import BronzeStorage


class BaseIngestion(ABC):
    """
    Base class implementing the Template Method Pattern.

    Every ingestion follows the same lifecycle:

        Fetch
            ↓
        Validate
            ↓
        Process Schema
            ↓
        Data Quality
            ↓
        Bronze Storage
    """

    source: str = "unknown"

    def __init__(self):

        # Infrastructure Services

        self.storage = BronzeStorage()

        self.schema_registry = SchemaRegistry(
            Path("data/metadata/schema_registry.json")
        )

        # Future

        # self.dq_engine = DQEngine(...)

    # ==========================================================
    # Template Method
    # ==========================================================

    def run(self):

        logger.info(
            "Starting {} ingestion job",
            self.source,
        )

        start = perf_counter()

        try:

            data = self._fetch_data()

            self._process_schema(data)

            self._run_data_quality(data)

            path = self._store_bronze(data)

            elapsed = perf_counter() - start

            logger.success(
                "{} ingestion completed in {:.3f} sec",
                self.source,
                elapsed,
            )

            return path

        except Exception as exc:

            logger.exception(exc)

            raise

    # ==========================================================
    # Workflow Steps
    # ==========================================================

    def _fetch_data(self):

        data = self.fetch()

        self.validate(data)

        return data

    def _process_schema(self, data):

        schema = SchemaUtils.infer_schema(data.payload)

        latest = self.schema_registry.latest(self.source)

        latest_schema = (
            {}
            if latest is None
            else latest["schema"]
        )

        diff = SchemaDiff.compare(
            latest_schema,
            schema,
        )

        if diff["added"] or diff["removed"] or diff["changed"]:
            logger.warning("Schema changes detected -> {}", diff)
        else:
            logger.info("No schema changes detected.")

        changed = self.schema_registry.register(
                self.source,
                schema,
            )

        if changed:

            logger.success(
                "Schema registry updated."
            )

    def _run_data_quality(self, data):

        """
        Placeholder.

        Sprint 13 integration.
        """

        pass

    def _store_bronze(self, data):

        return self.storage.save(
            source=self.source,
            data=data,
        )

    # ==========================================================
    # Child Responsibilities
    # ==========================================================

    @abstractmethod
    def fetch(self) -> Any:
        """
        Child classes implement data fetching.
        """

    def validate(self, data):

        if data is None:
            raise ValueError(
                "No data returned from fetch()."
            )