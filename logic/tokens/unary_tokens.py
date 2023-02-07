import re
import math
from typing import Union
from .primitive_tokens import Unary, Associativity


class UnaryLeft(Unary):
    """
    Class for tokens resembling unary operation located on the left side of operand
    """
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return Associativity.RTL


class UnaryRight(Unary):
    """
    Class for tokens resembling unary operation located on the right side of operand
    """
    @property
    def precedence(self):
        return 4


class UnaryMinus(UnaryLeft):
    """
    Class for tokens resembling mathematical negate operation
    """
    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        return -pack[0]

    @staticmethod
    def identity():
        return re.compile(fr"-")


class UnaryFactorial(UnaryRight):
    """
    Class for tokens resembling mathematical factorial operation
    """
    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        return math.gamma(pack[0] + 1)

    @staticmethod
    def identity():
        return re.compile(fr"!")
