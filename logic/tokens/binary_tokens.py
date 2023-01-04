import re
from logic import tokenizer


class BinaryPlus(tokenizer.Binary):
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


class BinaryMinus(tokenizer.Binary):
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


class BinaryMultiply(tokenizer.Binary):
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


class BinaryDivide(tokenizer.Binary):
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


class BinaryModulo(tokenizer.Binary):
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


class BinaryExponent(tokenizer.Binary):
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return tokenizer._Associativity.RTL

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return x ** y

    @staticmethod
    def pattern():
        return re.compile(fr"\^")
