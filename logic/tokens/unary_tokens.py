import re
import math
from .primitive_tokens import Unary, Associativity


class UnaryLeft(Unary):
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return Associativity.RTL


class UnaryRight(Unary):
    @property
    def precedence(self):
        return 4


class UnaryMinus(UnaryLeft):
    def operation(self, pack, **options):
        super().operation(pack)
        return -pack[0]

    @staticmethod
    def pattern():
        return re.compile(fr"-")


class UnaryFactorial(UnaryRight):
    def operation(self, pack, **options):
        super().operation(pack)
        return math.gamma(pack[0] + 1)

    @staticmethod
    def pattern():
        return re.compile(fr"!")
