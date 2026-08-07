from __future__ import annotations

import json 
from datetime import datetime,UTC
from pathlib import Path
from typing import Any

from dataclasses import asdict
from app.models.bronze_record import BronzeRecord

from app.core.config import settings
from app.core.logging import logger
from app.storage.manifest import Manifest
from app.storage.json_storage import JSONStorage

class BronzeStorage:
    """
    Responsible for persisting raw ingestion data
    into the Bronze layer
    """

    def __init__(self):
        self.base_path = settings.BRONZE_DIR
        self.storage = JSONStorage()

    def save(self, source:str, data:Any) -> Path:
        """
        Save raw data into the Bronze layer.
        """

        today = datetime.now()
        directory = self.base_path/f"source={source}"/"markets=general"/f"year={today.year}"/f"month={today.month:02d}"/f"day={today.day:02d}"
        directory.mkdir(
            parents= True,
            exist_ok= True
        )

        files = list(directory.glob("part-*.json"))
        next_number = len(files)+1
        filename = f"part-{next_number:06d}.json"
        file_path = directory/filename

        if isinstance(data, BronzeRecord):
            data = asdict(data)

        self.storage.save(
            data,
            file_path,
        )

        logger.success(f"Bronze file written -> {file_path}")

        file_info = {
            "path": str(file_path.relative_to(self.base_path)),
            "source": source,
            "market" : "general",
            "created_at": datetime.now(UTC).isoformat(),
            "size_bytes": file_path.stat().st_size

        }

        manifest = Manifest(self.base_path)
        manifest_data = manifest.load()
        manifest_data = manifest.update( manifest_data, file_info)
        manifest.save(manifest_data)
                                

        return file_path


