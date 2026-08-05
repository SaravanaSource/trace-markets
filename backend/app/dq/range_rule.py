"""
Range Rule

Validates that numeric fields fall within an expected range.

Examples
--------
price >= 0

percentage <= 100

age between 18 and 65
"""

from __future__ import annotations

from app.dq.base_rule import BaseRule
from app.dq.dq_result import DQResult


class RangeRule(BaseRule):
    """
    Validates numeric ranges for configured fields.
    """

    def __init__(
        self,
        ranges: dict[str, tuple[int | float | None, int | float | None]],
    ):
        self.ranges = ranges

    def validate(
        self,
        data: dict,
    ) -> DQResult:

        for field, (minimum, maximum) in self.ranges.items():

            # Missing fields are handled by RequiredRule
            if field not in data:
                continue

            value = data[field]

            # Ignore None values
            if value is None:
                continue

            # Skip non-numeric values.
            # DatatypeRule is responsible for type validation.
            if not isinstance(value, (int, float)):
                continue

            if minimum is not None and value < minimum:

                return DQResult(
                    passed=False,
                    rule=self.__class__.__name__,
                    message=(
                        f"Field '{field}' must be "
                        f">= {minimum}. "
                        f"Received {value}."
                    ),
                )

            if maximum is not None and value > maximum:

                return DQResult(
                    passed=False,
                    rule=self.__class__.__name__,
                    message=(
                        f"Field '{field}' must be "
                        f"<= {maximum}. "
                        f"Received {value}."
                    ),
                )

        return DQResult(
            passed=True,
            rule=self.__class__.__name__,
            message="Validation passed",
        )
