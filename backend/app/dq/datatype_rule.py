"""
Datatype Rule

Validates that fields contain values of the expected datatype.

Example
-------
Expected:

{
    "price": float,
    "volume": int,
    "symbol": str,
}

Record:

{
    "price": 1850.25,
    "volume": 100,
    "symbol": "INFY",
}
"""

from __future__ import annotations

from app.dq.base_rule import BaseRule
from app.dq.dq_result import DQResult


class DatatypeRule(BaseRule):
    """
    Validates runtime datatypes for selected fields.
    """

    def __init__(
        self,
        expected_types: dict[str, type],
    ):
        self.expected_types = expected_types

    def validate(
        self,
        data: dict,
    ) -> DQResult:

        for field, expected_type in self.expected_types.items():

            # Ignore fields that do not exist.
            # RequiredRule is responsible for mandatory fields.
            if field not in data:
                continue

            value = data[field]

            if value is None:
                continue

            if not isinstance(value, expected_type):

                return DQResult(
                    passed=False,
                    rule=self.__class__.__name__,
                    message=(
                        f"Field '{field}' expected "
                        f"{expected_type.__name__}, "
                        f"received {type(value).__name__}"
                    ),
                )

        return DQResult(
            passed=True,
            rule=self.__class__.__name__,
            message="Validation passed",
        )
