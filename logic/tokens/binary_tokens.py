import re
from .primitive_tokens import Binary, Associativity


class BinaryPlus(Binary):
    @property
    def precedence(self):
        return 1

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x + y

    @staticmethod
    def pattern():
        return re.compile(fr"\+")


class BinaryMinus(Binary):
    @property
    def precedence(self):
        return 1

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x - y

    @staticmethod
    def pattern():
        return re.compile(fr"-")


class BinaryMultiply(Binary):
    @property
    def precedence(self):
        return 2

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x * y

    @staticmethod
    def pattern():
        return re.compile(fr"\*")


class BinaryDivide(Binary):
    @property
    def precedence(self):
        return 2

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x / y

    @staticmethod
    def pattern():
        return re.compile(fr"/")


class BinaryModulo(Binary):
    @property
    def precedence(self):
        return 2

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x % y

    @staticmethod
    def pattern():
        return re.compile(fr"%")


class BinaryExponent(Binary):
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return Associativity.RTL

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x ** y

    @staticmethod
    def pattern():
        return re.compile(fr"\^")
