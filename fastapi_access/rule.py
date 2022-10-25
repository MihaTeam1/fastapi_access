from typing import List, Any, Tuple, Optional
from .operation import Operation
from .types import Operator


class Rule:
    def __init__(
            self,
            attr_path: str | List[str],
            first_value: Optional[Any] = None,
            operation: Optional[Operation] = None,
            second_value: Optional[Any] = None
    ):
        self.__attr_path = attr_path
        self.__first_value = first_value
        self.__operation = operation
        self.__second_value = second_value

    def __call__(self, initial_subject):
        first_value = self.__first_value
        second_value = self.__second_value
        if callable(self.__first_value):
            first_value = self.__first_value(initial_subject)
        else:
            first_value = self.__get_subject_value(initial_subject)
        if callable(self.__second_value):
            second_value = self.__second_value(initial_subject)
        if not second_value:
            return bool(first_value)
        return self.__operation(first_value, second_value)

    @staticmethod
    def __get_subject_attr(subject, path):
        if isinstance(subject, dict):
            subject = subject.get(path, None)
        else:
            subject = getattr(subject, path, None)
        return subject

    def __get_subject_value(self, subject):
        if type(self.__attr_path) is list:
            for path in self.__attr_path:
                subject = self.__get_subject_attr(subject, path)
                if subject is None:
                    break
        else:
            subject = self.__get_subject_attr(subject, self.__attr_path)
        return subject

    def __set_operation(self, operation: Tuple[Operator, Any]):
        if isinstance(operation[1], Rule):
            self.__first_value = Rule(
                attr_path=self.__attr_path,
                first_value=self.__first_value,
                operation=self.__operation,
                second_value=self.__second_value
            )
            self.__attr_path = ''
        elif self.__operation:
            raise ValueError('You cannot set more than one operation to rule')
        self.__operation = Operation(operation[0])
        self.__second_value = operation[1]

    def __and__(self, other):
        self.__set_operation((Operator.AND, other))
        return self

    def __or__(self, other):
        self.__set_operation((Operator.OR, other))
        return self

    def __eq__(self, other):
        self.__set_operation((Operator.EQUAL, other))
        return self

    def __ne__(self, other):
        self.__set_operation((Operator.NOT_EQUAL, other))
        return self

    def __gt__(self, other):
        self.__set_operation((Operator.GREATER, other))
        return self

    def __lt__(self, other):
        self.__set_operation((Operator.LOWER, other))
        return self

    def __ge__(self, other):
        self.__set_operation((Operator.EQ_GREATER, other))
        return self

    def __le__(self, other):
        self.__set_operation((Operator.EQ_LOWER, other))
        return self

    def contains(self, item):
        self.__set_operation((Operator.CONTAINS, item))
        return self

    def not_contains(self, item):
        self.__set_operation((Operator.NOT_CONTAINS, item))
        return self

    def in_(self, item: Any | List[Any]):
        self.__set_operation((Operator.IN, item))
        return self

    def not_in_(self, item: Any | List[Any]):
        self.__set_operation((Operator.NOT_IN, item))
        return self
