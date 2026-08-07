from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class JobContext:
    """
    Configuration required to execute a job.
    """

    name: str

    description: str
