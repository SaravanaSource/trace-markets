from app.dq.base_rule import BaseRule
from app.dq.dq_result import DQResult


class DQEngine:

    def __init__(self, rules: list[BaseRule]):
        self.rules = rules

    def validate(self, data: dict) -> list[DQResult]:

        results = []

        for rule in self.rules:

            result = rule.validate(data)

            results.append(result)

        return results
