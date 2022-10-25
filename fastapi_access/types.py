from enum import Enum


class Operator(Enum):
    EQUAL = '__eq__'
    NOT_EQUAL = '__ne__'
    GREATER = '__gt__'
    LOWER = '__lt__'
    EQ_GREATER = '__ge__'
    EQ_LOWER = '__le__'
    CONTAINS = 'contains'
    NOT_CONTAINS = 'not_contains'
    IN = 'in_'
    NOT_IN = 'not_in_'
    AND = '__and__'
    OR = '__or__'


