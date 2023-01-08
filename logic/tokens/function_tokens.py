from functools import reduce
import math
import re
from logic import tokenizer


# unlimited arg (arg list are more over reduced to single value)
class FunctionModulo(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a % b, pack)

    @staticmethod
    def pattern():
        return re.compile(fr"MOD", re.I)


class FunctionFloorDivision(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + (reduce(lambda a, b: a // b, pack) if len(pack) > 1 else pack[0] // 1)

    @staticmethod
    def pattern():
        return re.compile(fr"FDIV", re.I)


class FunctionMin(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + min(pack)

    @staticmethod
    def pattern():
        return re.compile(fr"MIN", re.I)


class FunctionMax(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + max(pack)

    @staticmethod
    def pattern():
        return re.compile(fr"MAX", re.I)


class FunctionRoot(tokenizer.Function):
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: a ** (1/b), pack) if len(pack) > 1 else pack[0] ** 0.5)

    @staticmethod
    def pattern():
        return re.compile(fr"ROOT", re.I)


class FunctionPow(tokenizer.Function):
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: a ** b, pack) if len(pack) > 1 else pack[0] ** 2)

    @staticmethod
    def pattern():
        return re.compile(fr"POW", re.I)


class FunctionLog(tokenizer.Function):
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + (reduce(lambda a, b: math.log(a, b), pack) if len(pack) > 1 else math.log10(pack[0]))

    @staticmethod
    def pattern():
        return re.compile(fr"LOG", re.I)


class FunctionAdd(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + sum(pack)

    @staticmethod
    def pattern():
        return re.compile(fr"ADD", re.I)


class FunctionSubtract(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a - b, pack)

    @staticmethod
    def pattern():
        return re.compile(fr"SUB", re.I)


class FunctionMultiply(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a * b, pack)

    @staticmethod
    def pattern():
        return re.compile(fr"MUL", re.I)


class FunctionDivide(tokenizer.Function):
    def operation(self, pack, **options):
        return super().operation(pack) + reduce(lambda a, b: a / b, pack)

    @staticmethod
    def pattern():
        return re.compile(fr"DIV", re.I)


# 1 arg only
class FunctionSin(tokenizer.Function):
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.sin(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def pattern():
        return re.compile(fr"SIN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionCos(tokenizer.Function):
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.cos(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def pattern():
        return re.compile(fr"COS", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionTan(tokenizer.Function):
    def operation(self, pack, **options):
        rad: bool = options.get('rad') or False
        return super().operation(pack) + math.tan(pack[0] if not rad else math.radians(pack[0]))

    @staticmethod
    def pattern():
        return re.compile(fr"TAN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class FunctionLn(tokenizer.Function):
    def operation(self, pack, **options):
        s = super().operation(pack)
        return s + math.log(pack[0], math.e)

    @staticmethod
    def pattern():
        return re.compile(fr"LN", re.I)

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1