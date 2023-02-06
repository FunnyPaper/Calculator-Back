import math
import re
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import TypeVar, Union
from ..errors import OperationArgumentsException


@dataclass(frozen=True)
class Token(ABC):
    """
    Base class for token creation
    """
    value: str
    begin: int
    end: int

    @staticmethod
    @abstractmethod
    def identity() -> re.Pattern:
        """
        Token regex identity

        :return: Regex pattern object resembling token
        """
        pass

    def __post_init__(self) -> None:
        """
        Verifies token identity
        """
        if not type(self).identity().match(self.value):
            raise ValueError(f"Invalid Token value for Token group {type(self)}")


class _Special(Token):
    """
    Base class for tokens requiring special treatment
    """
    pass


class OpenBracket(_Special):
    """
    Class for tokens resembling any open bracket (either "(", "[" or "{")
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(r"[({\[]")


class CloseBracket(_Special):
    """
    Class for tokens resembling any close bracket (either ")", "]" or "}")
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(r"[)}\]]")


class EndAnchor(_Special):
    """
    Class for tokens resembling end of a string
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(r"$")


class StartAnchor(_Special):
    """
    Class for tokens resembling start of a string
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(r"^")


class AnyChar(_Special):
    """
    Class for tokens resembling entire not empty string
    """
    @staticmethod
    def identity() -> re.Pattern:
        return re.compile(".+")


class Operand(Token):
    """
    Base class for tokens resembling operands
    """
    @property
    @abstractmethod
    def cast(self) -> float:
        """
        Casts associated value to float

        :return: Token representation as float
        """
        pass


class Associativity(IntEnum):
    """
    Enum for operator tokens associativity
    """
    LTR = 0
    RTL = 1


class Operator(Token):
    """
    Base class for tokens resembling operators
    """
    @property
    @abstractmethod
    def precedence(self) -> int:
        """
        Operator precedence in mathematical expression

        :return: Token precedence
        """
        pass

    @property
    def associativity(self) -> Associativity:
        """
        Operator associativity in mathematical expression

        :return: Token associativity
        """
        return Associativity.LTR

    @abstractmethod
    def operation(self, pack: list[float], **options: Union[bool, str]) -> float:
        """
        Calls defined operation on the pack of arguments

        :param pack: Operands (casted operand tokens)
        :param options: Parameters for modification of operation process
        :return: Result of operation
        """
        # Enforce given arguments number to lie between bounds
        x, y = self.args_min_max
        if not (x <= len(pack) <= y):
            raise OperationArgumentsException('To much operands passed')

        return 0

    @property
    def args_min_max(self) -> tuple[float, float]:
        """
        Operator arguments limit

        :return: Minimum, maximum limit
        """
        return 1, math.inf


class Binary(Operator):
    """
    Base class for resembling binary operators
    """
    @property
    def args_min_max(self) -> tuple[float, float]:
        return 2, 2


class Unary(Operator):
    """
    Base class for tokens resembling unary operators
    """
    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class Function(Operator):
    """
    Base class for tokens resembling mathematical functions
    """
    @property
    def precedence(self) -> int:
        return 5


# Helper types
Token_t = TypeVar('Token_t', bound=Token)
Operator_T = TypeVar('Operator_T', bound=Operator)
Operand_T = TypeVar('Operand_T', bound=Operand)
