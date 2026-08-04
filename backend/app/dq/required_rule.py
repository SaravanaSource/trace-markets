from app.dq.base_rule import BaseRule
from app.dq.dq_result import DQResult

class RequiredRule(BaseRule):
    """
    Validates that required fields exist and are not None.
    """

    def __init__(self, required_fields : list[str]):
        self.required_fields = required_fields

    def validate(self, data: dict) -> DQResult:
        for field in self.required_fields:

            if field not in data:
                return DQResult(
                    passed= False,
                    rule= self.__class__.__name__,
                    message= f"Missing required field {field}"
                )
            
            if data[field] is None:
            
                return DQResult(
                    passed= False,
                    rule= self.__class__.__name__,
                    message= f"{field} field cannot be None"
                )
            
        return DQResult(
            passed=True,
            rule=self.__class__.__name__,
            message="Validation passed"
        )