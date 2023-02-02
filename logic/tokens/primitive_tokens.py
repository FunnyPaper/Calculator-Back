import math
import re
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import TypeVar, Union


@dataclass(frozen=True)
class Token(ABC):
    value: str
    begin: int
    end: int

    @staticmethod
    @abstractmethod
    def pattern() -> re.Pattern:
        pass

    def __post_init__(self):
        if not type(self).pattern().match(self.value):
            raise ValueError(f"Invalid Token value for Token group {type(self)}")


class _Special(Token):
    pass


class OpenBracket(_Special):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(r"[({\[]")


class CloseBracket(_Special):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(r"[)}\]]")


class EndAnchor(_Special):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(r"$")


class StartAnchor(_Special):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(r"^")


class AnyChar(_Special):
    @staticmethod
    def pattern() -> re.Pattern:
        return re.compile(".+")


class Operand(Token):
    @property
    @abstractmethod
    def cast(self) -> float:
        pass


class Associativity(IntEnum):
    LTR = 0
    RTL = 1


class Operator(Token):
    @property
    @abstractmethod
    def precedence(self) -> int:
        pass

    @property
    def associativity(self) -> Associativity:
        return Associativity.LTR

    @abstractmethod
    def operation(self, pack: list[float], **options: Union[bool, str]) -> float:
        x, y = self.args_min_max
        if not (x <= len(pack) <= y):
            raise ValueError('To much operands passed')

        return 0

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, math.inf


class Binary(Operator):
    @property
    def args_min_max(self) -> tuple[float, float]:
        return 2, 2


class BinaryComma(Binary):
    @property
    def precedence(self):
        return 0

    def operation(self, pack, **options):
        super().operation(pack)
        x, y = pack
        return ([*x] if isinstance(x, list) else [x]) + ([*y] if isinstance(y, list) else [y])

    @staticmethod
    def pattern():
        return re.compile(fr",")


class Unary(Operator):
    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class Function(Operator):
    @property
    def precedence(self) -> int:
        return 5


Token_t = TypeVar('Token_t', bound=Token)
Operator_T = TypeVar('Operator_T', bound=Operator)
Operand_T = TypeVar('Operand_T', bound=Operand)
