from dataclasses import dataclass


@dataclass
class DQResult:
    """
    Represents the outcome of one Data Quality rule.
    """

    passed: bool
    rule: str
    message: str
