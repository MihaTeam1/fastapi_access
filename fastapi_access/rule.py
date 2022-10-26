from collections.abc import Iterable
from typing import List, Any, Tuple, Optional
from .operation import Operation
from .types import Operator


class Rule:
    def __init__(
            self,
            *attr_path: str,
            first_value: Optional[Any] = None,
            operation: Optional[Operation] = None,
            second_value: Optional[Any] = None
    ):
        self._attr_path = attr_path
        self._first_value = first_value
        self._operation = operation
        self._second_value = second_value

    def __call__(self, initial_subject):
        first_value = self._first_value
        second_value = self._second_value
        if callable(first_value):
            first_value = first_value(initial_subject)
        else:
            first_value = self.__get_subject_value(initial_subject)
        if callable(second_value):
            second_value = second_value(initial_subject)
        if self._operation is None:
            return first_value
        result = self._operation(first_value, second_value)
        return result

    @classmethod
    def __get_subject_attr(cls, subject, path):
        if isinstance(subject, dict):
            subject = subject.get(path, None)
        elif isinstance(subject, list):
            subject = cls.__join_attr_list_values(subject, path)
        else:
            subject = getattr(subject, path, None)
        return subject

    @classmethod
    def __join_attr_list_values(cls, subject, path):
        result = []
        for item in subject:
            result.append(cls.__get_subject_attr(item, path))
        return result

    def __get_subject_value(self, subject):
        for path in self._attr_path:
            subject = self.__get_subject_attr(subject, path)
        return subject

    def __set_operation(self, operation: Tuple[Operator, Any]):
        if isinstance(operation[1], Rule):
            self._first_value = Rule(
                *self._attr_path,
                first_value=self._first_value,
                operation=self._operation,
                second_value=self._second_value
            )
            self.__attr_path = []
        elif self._operation:
            raise ValueError('You cannot set more than one operation to rule')
        self._operation = Operation(operation[0])
        self._second_value = operation[1]

    def __and__(self, other) -> 'Rule':
        self.__set_operation((Operator.AND, other))
        return self

    def __or__(self, other) -> 'Rule':
        self.__set_operation((Operator.OR, other))
        return self

    def __eq__(self, other) -> 'Rule':
        self.__set_operation((Operator.EQUAL, other))
        return self

    def __ne__(self, other) -> 'Rule':
        self.__set_operation((Operator.NOT_EQUAL, other))
        return self

    def __gt__(self, other) -> 'Rule':
        self.__set_operation((Operator.GREATER, other))
        return self

    def __lt__(self, other) -> 'Rule':
        self.__set_operation((Operator.LOWER, other))
        return self

    def __ge__(self, other) -> 'Rule':
        self.__set_operation((Operator.EQ_GREATER, other))
        return self

    def __le__(self, other) -> 'Rule':
        self.__set_operation((Operator.EQ_LOWER, other))
        return self

    def contains(self, item) -> 'Rule':
        self.__set_operation((Operator.CONTAINS, item))
        return self

    def not_contains(self, item) -> 'Rule':
        self.__set_operation((Operator.NOT_CONTAINS, item))
        return self

    def in_(self, item: Any | List[Any]) -> 'Rule':
        self.__set_operation((Operator.IN, item))
        return self

    def not_in_(self, item: Any | List[Any]) -> 'Rule':
        self.__set_operation((Operator.NOT_IN, item))
        return self