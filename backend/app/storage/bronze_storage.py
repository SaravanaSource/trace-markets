from __future__ import annotations

import json 
from datetime import datetime
from pathlib import Path
from typing import Any

from dataclasses import asdict
from app.models.bronze_record import BronzeRecord

from app.core.config import settings
from app.core.logging import logger

class BronzeStorage:
    """
    Responsible for persisting raw ingestion data
    into the Bronze layer
    """

    def save(self, source:str, data:Any) -> Path:
        """
        Save raw data into the Bronze layer.

        Example:
        data/
        └── bronze/
            └── nse/
                └── 2026-08-01/
                    └── 20260801_104512.json
        """

        today = datetime.now().strftime("%Y-%m-%d")
        directory = settings.BRONZE_DIR/source/today
        directory.mkdir(
            parents= True,
            exist_ok= True
        )
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")
        file_path = directory/filename

        if isinstance(data, BronzeRecord):
            data = asdict(data)

        with open(file_path, 'w', encoding= 'utf-8' ) as file:
            json.dump(
                data,
                file,
                ensure_ascii= False,
                indent=4
            )

        logger.success(f"Bronze file written -> {file_path}")
        return file_path

