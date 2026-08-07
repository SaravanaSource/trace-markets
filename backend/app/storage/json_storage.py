from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.storage.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """
    JSON storage engine.
    """

    def save(
        self,
        data: Any,
        path: Path,
    ) -> Path:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                default=str,
            )

        return path

    def load(
        self,
        path: Path,
    ) -> Any:

        with path.open(
            encoding="utf-8",
        ) as file:

            return json.load(file)
