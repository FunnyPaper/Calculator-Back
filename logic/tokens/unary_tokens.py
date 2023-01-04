import re
import math
from logic import tokenizer


class UnaryLeft(tokenizer.Unary):
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return tokenizer._Associativity.RTL


class UnaryRight(tokenizer.Unary):
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
