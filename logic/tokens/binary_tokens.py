import re
from typing import Union
from .primitive_tokens import Binary, Associativity


class BinaryComma(Binary):
    """
    Class for tokens resembling function argument separator
    """
    @property
    def precedence(self):
        return 0

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return ([*x] if isinstance(x, list) else [x]) + ([*y] if isinstance(y, list) else [y])

    @staticmethod
    def identity():
        return re.compile(fr",")


class BinaryPlus(Binary):
    """
    Class for tokens resembling mathematical add operation
    """
    @property
    def precedence(self):
        return 1

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x + y

    @staticmethod
    def identity():
        return re.compile(fr"\+")


class BinaryMinus(Binary):
    """
    Class for tokens resembling mathematical subtract operation
    """
    @property
    def precedence(self):
        return 1

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x - y

    @staticmethod
    def identity():
        return re.compile(fr"-")


class BinaryMultiply(Binary):
    """
    Class for tokens resembling mathematical multiply operation
    """
    @property
    def precedence(self):
        return 2

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x * y

    @staticmethod
    def identity():
        return re.compile(fr"\*")


class BinaryDivide(Binary):
    """
    Class for tokens resembling mathematical divide operation
    """
    @property
    def precedence(self):
        return 2

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x / y

    @staticmethod
    def identity():
        return re.compile(fr"/")


class BinaryModulo(Binary):
    """
    Class for tokens resembling mathematical modulo operation
    """
    @property
    def precedence(self):
        return 2

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x % y

    @staticmethod
    def identity():
        return re.compile(fr"%")


class BinaryExponent(Binary):
    """
    Class for tokens resembling mathematical power operation
    """
    @property
    def precedence(self):
        return 3

    @property
    def associativity(self):
        return Associativity.RTL

    def operation(self, pack: list[float], **options: Union[bool, str]):
        super().operation(pack)
        x, y = pack
        return x ** y

    @staticmethod
    def identity():
        return re.compile(fr"\^")
