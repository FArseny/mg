from enum import Enum
from typing import Callable, Union
from operator import add, sub, mul, truediv


class Operator(Enum):
    PLUS     = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE   = '/'


def getOperFunc(op: str) -> Callable[[int, int], Union[int, float]]:
    if op == Operator.PLUS.value:     return add
    if op == Operator.SUBTRACT.value: return sub
    if op == Operator.MULTIPLY.value: return mul
    if op == Operator.DIVIDE.value:   return truediv