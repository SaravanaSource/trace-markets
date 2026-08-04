"""
Schema Registry

Maintains schema history for every ingestion source.

Responsibilities
----------------
- Persist schema metadata
- Track schema versions
- Maintain schema history
- Provide latest schema
- Detect new sources

This module intentionally knows nothing about finance,
markets, or business logic.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from loguru import logger


class SchemaRegistry:
    """
    Stores schema history for all ingestion sources.
    """

    def __init__(self, registry_path: Path):
        self.registry_path = registry_path

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def load(self) -> dict[str, Any]:
        """
        Load registry from disk.

        Returns an empty registry if it does not exist.
        """

        if not self.registry_path.exists():
            logger.info(
                "Schema registry not found. Creating new registry in memory."
            )
            return self._empty_registry()

        with self.registry_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            registry = json.load(file)

        logger.debug(
            "Loaded schema registry from {}",
            self.registry_path,
        )

        return registry

    def save(self, registry: dict[str, Any]) -> None:
        """
        Persist registry to disk.
        """

        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.registry_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.success(
            "Schema registry updated -> {}",
            self.registry_path,
        )

    def exists(
        self,
        source: str,
    ) -> bool:
        """
        Returns True if source exists.
        """

        registry = self.load()

        return source in registry["sources"]

    def latest(
        self,
        source: str,
    ) -> dict[str, Any] | None:
        """
        Returns latest schema version for a source.

        Returns None if source has never been registered.
        """

        registry = self.load()

        if source not in registry["sources"]:
            return None

        history = registry["sources"][source]["history"]

        if not history:
            return None

        return history[-1]

    def history(
        self,
        source: str,
    ) -> list[dict[str, Any]]:
        """
        Returns complete schema history.
        """

        registry = self.load()

        if source not in registry["sources"]:
            return []

        return registry["sources"][source]["history"]

    def register(
        self,
        source: str,
        schema: dict[str, str],
    ) -> bool:
        """
        Register a schema.

        Returns
        -------
        True
            New schema version created.

        False
            Schema already exists.
        """

        registry = self.load()

        # -----------------------------------------------------
        # First time source
        # -----------------------------------------------------

        if source not in registry["sources"]:

            logger.info(
                "Registering first schema for source '{}'",
                source,
            )

            registry["sources"][source] = {
                "current_version": 1,
                "history": [
                    {
                        "version": 1,
                        "registered_at": datetime.now(
                            UTC
                        ).isoformat(),
                        "schema": deepcopy(schema),
                    }
                ],
            }

            self.save(registry)

            return True

        # -----------------------------------------------------
        # Existing source
        # -----------------------------------------------------

        latest_schema = registry["sources"][source]["history"][-1][
            "schema"
        ]

        if latest_schema == schema:

            logger.info(
                "No schema change detected for '{}'",
                source,
            )

            return False

        current_version = registry["sources"][source][
            "current_version"
        ]

        next_version = current_version + 1

        logger.warning(
            "Schema change detected for '{}'. "
            "Registering version {}",
            source,
            next_version,
        )

        registry["sources"][source]["history"].append(
            {
                "version": next_version,
                "registered_at": datetime.now(
                    UTC
                ).isoformat(),
                "schema": deepcopy(schema),
            }
        )

        registry["sources"][source][
            "current_version"
        ] = next_version

        self.save(registry)

        return True

    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _empty_registry() -> dict[str, Any]:
        """
        Create an empty registry structure.
        """

        return {
            "version": 1,
            "sources": {},
        }