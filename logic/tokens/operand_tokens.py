import math
import re
from logic import tokenizer


class Number(tokenizer._Operand):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(fr"\d+(?:\.\d+)?(?:e(?:-|\+)\d+)?")

    @property
    def cast(self):
        return float(self.value)


class Constant(tokenizer._Operand):
    pass


class PIConstant(Constant):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(fr"PI", re.I)

    @property
    def cast(self):
        return math.pi


class EConstant(Constant):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(fr"E", re.I)

    @property
    def cast(self):
        return math.e
