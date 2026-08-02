from pathlib import Path
import json
from datetime import datetime,UTC

class Manifest:
    """
    Maintains metadata about the Bronze Data Lake.
    """
    def __init__(self, base_path: Path):
        self.basepath = base_path
        self.manifest_file = base_path/"_manifest.json"

    def load(self):
        """
        Load the manifest from disk.
        If it doesn't exist, return an empty manifest.
        """
        if not self.manifest_file.exists():
            return {
                "version": 1,
                "last_updated": None,
                "total_files": 0,
                "files": [],
            }
        
        with open(self.manifest_file,'r', encoding='utf-8' ) as file:
            return json.load(file)
        

    def update(self, manifest :dict, file_info:dict):
        """
        Update the manifest with a newly created Bronze file.
        """
        manifest["files"].append(file_info)
        manifest["total_files"] += 1
        manifest['last_updated'] = datetime.now(UTC).isoformat() 
        return manifest
        

    def save(self, manifest:dict):
        """
        save the manifest to disk
        """

        with self.manifest_file.open('w', encoding='utf-8') as file:
            json.dump(
                manifest,
                file,
                indent=4
            )