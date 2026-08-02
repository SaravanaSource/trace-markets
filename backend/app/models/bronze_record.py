from typing import Any
from dataclasses import dataclass

@dataclass
class BronzeRecord:
    """
    Represents one Bronze layer record
    """
    
    metadata: dict[str:Any]
    payload: Any