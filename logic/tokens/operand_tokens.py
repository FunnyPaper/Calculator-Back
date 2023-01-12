import math
import re
from logic.tokens.primitive_tokens import _Operand


class Number(_Operand):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(fr"\d+(?:\.\d+)?(?:e(?:-|\+)\d+)?")

    @property
    def cast(self):
        return float(self.value)


class Constant(_Operand):
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
