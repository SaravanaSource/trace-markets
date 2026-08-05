from app.dq.base_rule import BaseRule
from app.dq.dq_result import DQResult
from app.dq.rule_report import RuleReport



class DQEngine:

    def __init__(self, rules: list[BaseRule]):
        self.rules = rules


    def validate(self, data: dict) -> RuleReport:

        report = RuleReport()

        for rule in self.rules:
            report.results.append(
                rule.validate(data)
            )

        return report
