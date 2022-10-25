from typing import List, Any, Tuple, Optional
from .operation import Operation
from .types import Operator


class Rule:
    def __init__(
            self,
            attr_path: Optional[str | List[str]],
            __operation: Optional[Operation] = None
    ):
        self.__attr_path = attr_path
        self.__operation = __operation
        self.__rules_operation = False
        self.__main_rule = self

    def __call__(self, subject):
        if self.__rules_operation:
            result = self.__operation(
                subject,
                self.__main_rule,
            )
        else:
            result = self.__operation(self.__get_subject_value(subject))
        return result

    @staticmethod
    def __get_subject_attr(subject, path):
        subject = subject.copy()
        if isinstance(subject, dict):
            subject = subject.get(path, None)
        else:
            subject = getattr(subject, path, None)
        return subject

    def __get_subject_value(self, subject):
        subject = subject.copy()
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
            self.__rules_operation = True
            self.__main_rule = Rule(
                attr_path=self.__attr_path,
                __operation=self.__operation
            )
        elif self.__operation:
            raise ValueError('You cannot set more than one operation to rule')
        self.__operation = Operation(
            operation_type=operation[0],
            operation_value=operation[1],
        )

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

    def in_(self, item: Any | List[Any]):
        self.__set_operation((Operator.IN, item))
        return self
