import math
import re
from .primitive_tokens import Operand


class Number(Operand):
    """
    Class for tokens resembling numeric operands
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(fr"\d+(?:\.\d+)?(?:e(?:-|\+)\d+)?")

    @property
    def cast(self):
        return float(self.value)


class Constant(Operand):
    """
    Class for tokens resembling mathematical constants
    """
    pass


class PIConstant(Constant):
    """
    Class for tokens resembling PI mathematical constant
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(fr"PI", re.I)

    @property
    def cast(self):
        return math.pi


class EConstant(Constant):
    """
    Class for tokens resembling E mathematical constant
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(fr"E", re.I)

    @property
    def cast(self):
        return math.e
