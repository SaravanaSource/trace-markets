from __future__ import annotations

from dataclasses import dataclass, field

from app.dq.dq_result import DQResult


@dataclass(slots=True)
class RuleReport:
    """
    Aggregated result of all Data Quality rules.
    """

    results: list[DQResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def success(self) -> bool:
        return self.failed == 0
