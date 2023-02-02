from functools import reduce
import math
import re
from .primitive_tokens import Function


# Unlimited arg (arg list are more over reduced to single value)
class FunctionModulo(Function):
    """
    Class for tokens resembling mathematical modulo function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a % b, pack)

    @staticmethod
    def identity():
        return re.compile(fr"MOD", re.I)


class FunctionFloorDivision(Function):
    """
    Class for tokens resembling mathematical floor division function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + (reduce(lambda a, b: a // b, pack) if len(pack) > 1 else pack[0] // 1)

    @staticmethod
    def identity():
        return re.compile(fr"FDIV", re.I)


class FunctionMin(Function):
    """
    Class for tokens resembling mathematical minimum function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + min(pack)

    @staticmethod
    def identity():
        return re.compile(fr"MIN", re.I)


class FunctionMax(Function):
    """
    Class for tokens resembling mathematical maximum function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + max(pack)

    @staticmethod
    def identity():
        return re.compile(fr"MAX", re.I)


class FunctionRoot(Function):
    """
    Class for tokens resembling mathematical root function
    """
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: a ** (1/b), pack) if len(pack) > 1 else pack[0] ** 0.5)

    @staticmethod
    def identity():
        return re.compile(fr"ROOT", re.I)


class FunctionPow(Function):
    """
    Class for tokens resembling mathematical power function
    """
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: a ** b, pack) if len(pack) > 1 else pack[0] ** 2)

    @staticmethod
    def identity():
        return re.compile(fr"POW", re.I)


class FunctionLog(Function):
    """
    Class for tokens resembling mathematical logarithm function
    """
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: math.log(a, b), pack) if len(pack) > 1 else math.log10(pack[0]))

    @staticmethod
    def identity():
        return re.compile(fr"LOG", re.I)


class FunctionAdd(Function):
    """
    Class for tokens resembling mathematical add function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + sum(pack)

    @staticmethod
    def identity():
        return re.compile(fr"ADD", re.I)


class FunctionSubtract(Function):
    """
    Class for tokens resembling mathematical subtract function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a - b, pack)

    @staticmethod
    def identity():
        return re.compile(fr"SUB", re.I)


class FunctionMultiply(Function):
    """
    Class for tokens resembling mathematical multiply function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a * b, pack)

    @staticmethod
    def identity():
        return re.compile(fr"MUL", re.I)


class FunctionDivide(Function):
    """
    Class for tokens resembling mathematical divide function
    """
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a / b, pack)

    @staticmethod
    def identity():
        return re.compile(fr"DIV", re.I)


# Functions taking one argument
class FunctionSin(Function):
    """
    Class for tokens resembling mathematical sine function
    """
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.sin(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def identity():
        return re.compile(fr"SIN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionCos(Function):
    """
    Class for tokens resembling mathematical cosine function
    """
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.cos(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def identity():
        return re.compile(fr"COS", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionTan(Function):
    """
    Class for tokens resembling mathematical tangent function
    """
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.tan(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def identity():
        return re.compile(fr"TAN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionLn(Function):
    """
    Class for tokens resembling mathematical natural logarithm function
    """
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + math.log(pack[0], math.e)

    @staticmethod
    def identity():
        return re.compile(fr"LN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1
