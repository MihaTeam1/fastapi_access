from typing import Optional, Any, Callable, TYPE_CHECKING
from .types import Operator


if TYPE_CHECKING:
    from .rule import Rule


class Operation:
    def __init__(self, operation_type: Operator):
        self.__operation = self.__get_operation_method(operation_type)

    def __call__(
            self,
            first_value: Optional[Any] = None,
            second_value: Optional[Any] = None
    ):

        return self.__operation(first_value, second_value)

    @classmethod
    def __get_operation_method(cls, operation_type) -> Callable:
        match operation_type:
            case Operator.AND:
                return cls.__perform_and
            case Operator.OR:
                return cls.__perform_or
            case Operator.EQUAL:
                return cls.__perform_equality
            case Operator.NOT_EQUAL:
                return cls.__perform_not_equality
            case Operator.GREATER:
                return cls.__perform_higher
            case Operator.LOWER:
                return cls.__perform_lower
            case Operator.EQ_GREATER:
                return cls.__perform_eq_higher
            case Operator.EQ_LOWER:
                return cls.__perform_eq_lower
            case Operator.CONTAINS:
                return cls.__perform_contains
            case Operator.NOT_CONTAINS:
                return cls.__perform_not_contains
            case Operator.IN:
                return cls.__perform_in
            case Operator.NOT_IN:
                return cls.__perform_not_in
            case _:
                raise ValueError(f'Operation Type: "{self.__operation_type}" - is not available')

    @staticmethod
    def __perform_and(value, second_value) -> bool:
        return value and second_value

    @staticmethod
    def __perform_or(value, second_value) -> bool:
        return value or second_value

    @staticmethod
    def __perform_equality(value, second_value) -> bool:
        return value == second_value

    @staticmethod
    def __perform_not_equality(value, second_value) -> bool:
        return value != second_value

    @staticmethod
    def __perform_higher(value, second_value) -> bool:
        return value > second_value

    @staticmethod
    def __perform_lower(value, second_value) -> bool:
        return value < second_value

    @staticmethod
    def __perform_eq_higher(value, second_value) -> bool:
        return value >= second_value

    @staticmethod
    def __perform_eq_lower(value, second_value) -> bool:
        return value <= second_value

    @staticmethod
    def __perform_contains(value, second_value) -> bool:
        return second_value in value

    @staticmethod
    def __perform_not_contains(value, second_value) -> bool:
        return second_value not in value

    @staticmethod
    def __perform_in(value, second_value) -> bool:
        return value in second_value

    @staticmethod
    def __perform_not_in(value, second_value) -> bool:
        return value not in second_value
