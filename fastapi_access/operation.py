from typing import Optional, Any, Callable, TYPE_CHECKING
from .types import Operator


if TYPE_CHECKING:
    from .rule import Rule


class Operation:
    def __init__(
            self,
            operation_type: Operator,
            operation_value: Optional[Any] = None,
            rule_operation: bool = False
    ):

        if not operation_value:
            raise ValueError('Not boolean operation requires value')
        self.__operation_type = operation_type
        self.__operation_value = operation_value
        self.__operation = self.__get_operation_method()
        self.rule_operation = rule_operation

    def __perform_rules(self, rule, subject):
        self.__operation_value = self.__operation_value(subject)
        return rule(subject)

    def __str__(self):
        return f'{self.__operation_type}, {self.__operation_value}'

    def __call__(self, value: Optional[Any] = None, rule: Optional['Rule'] = None):
        if rule:
            value = self.__perform_rules(rule, value)
        return self.__operation(value)

    def __get_operation_method(self) -> Callable:
        match self.__operation_type:
            case Operator.EQUAL:
                return self.__perform_equality
            case Operator.NOT_EQUAL:
                return self.__perform_not_equality
            case Operator.GREATER:
                return self.__perform_higher
            case Operator.LOWER:
                return self.__perform_lower
            case Operator.EQ_GREATER:
                return self.__perform_eq_higher
            case Operator.EQ_LOWER:
                return self.__perform_eq_lower
            case Operator.CONTAINS:
                return self.__perform_contains
            case Operator.IN:
                return self.__perform_in
            case Operator.TRUE:
                return self.__perform_true
            case Operator.FALSE:
                return self.__perform_false
            case _:
                raise ValueError(f'Operation Type: "{self.__operation_type}" - is not available')

    def __perform_equality(self, value) -> bool:
        return value == self.__operation_value

    def __perform_not_equality(self, value) -> bool:
        return value != self.__operation_value

    def __perform_higher(self, value) -> bool:
        return value > self.__operation_value

    def __perform_lower(self, value) -> bool:
        return value < self.__operation_value

    def __perform_eq_higher(self, value) -> bool:
        return value >= self.__operation_value

    def __perform_eq_lower(self, value) -> bool:
        return value <= self.__operation_value

    def __perform_contains(self, value) -> bool:
        return self.__operation_value in value

    def __perform_in(self, value) -> bool:
        return value in self.__operation_value

    def __perform_true(self, value) -> bool:
        return value

    def __perform_false(self, value) -> bool:
        return not value
