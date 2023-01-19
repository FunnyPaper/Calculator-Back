import math
import re
from .primitive_tokens import Operand


class Number(Operand):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(fr"\d+(?:\.\d+)?(?:e(?:-|\+)\d+)?")

    @property
    def cast(self):
        return float(self.value)


class Constant(Operand):
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
