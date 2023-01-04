import math
from collections.abc import Sequence
import re
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import TypeVar, Callable, Union


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


class _Operand(Token):
    @property
    @abstractmethod
    def cast(self) -> float:
        pass


class _Associativity(IntEnum):
    LTR = 0
    RTL = 1


class _Operator(Token):
    @property
    @abstractmethod
    def precedence(self) -> int:
        pass

    @property
    def associativity(self) -> _Associativity:
        return _Associativity.LTR

    @abstractmethod
    def operation(self, pack: list[float], **options: Union[bool, str]) -> float:
        x, y = self.args_min_max
        if not (x <= len(pack) <= y):
            raise ValueError('To much operands passed')

        return 0

    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, math.inf


class Binary(_Operator):
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


class Unary(_Operator):
    @property
    def args_min_max(self) -> tuple[float, float]:
        return 1, 1


class Function(_Operator):
    @property
    def precedence(self) -> int:
        return 5


Token_t = TypeVar('Token_t', bound=Token)
Operator_T = TypeVar('Operator_T', bound=_Operator)
Operand_T = TypeVar('Operand_T', bound=_Operand)


class Rule:
    __group: Sequence[Token_t, ...] = []
    __before: list[Token_t, ...] = []
    __after: list[Token_t, ...] = []

    def __init__(self, group: Sequence[Token_t, ...]):
        if len(group) == 0:
            raise ValueError("Rule cannot be empty")

        self.__group = group

    @property
    def group(self) -> Sequence[Token_t, ...]:
        return self.__group

    def add(self, *, before: Sequence[Token_t, ...] = None, after: Sequence[Token_t, ...] = None):
        self.__before = [*self.__before, *(before or [])]
        self.__after = [*self.__after, *(after or [])]

    def compile(self) -> re.Pattern:
        before = '|'.join(map(lambda x: x.pattern().pattern, self.__before))
        if len(before) > 0:
            before = fr"(?<={before})"

        after = '|'.join(map(lambda x: x.pattern().pattern, self.__after))
        if len(after) > 0:
            after = fr"(?={after})"

        group = '|'.join(map(lambda x: x.pattern().pattern, self.__group))
        return re.compile(fr"{before}({group}){after}", re.I)


class Tokenizer:
    __rules: dict[str, Rule] = dict()
    __tokens: list[Token_t] = None
    __validators: tuple[Callable[[list[Token_t]], None]]
    __pattern: re.Pattern = None

    @property
    def tokens(self) -> list[Token_t]:
        return self.__tokens

    def set_rules(self, **kwargs: Rule):
        for k, v in kwargs.items():
            if not isinstance(v, Rule):
                raise ValueError(f"{k} rule must be an instance of {Rule} or one of it's subclass", str(v))

        self.__rules.update(kwargs)

    def set_validators(self, *validators: Callable[[list[Token_t]], None]):
        self.__validators = validators

    def parse(self, expression: str) -> Sequence[Token_t, ...]:
        tokens = self.__tokenize(self.__split(expression))
        self.verify()

        return tokens

    def verify(self):
        for validator in self.__validators:
            validator(self.__tokens[:])

    def compile(self):
        self.__rules["invalid"] = Rule([AnyChar])
        self.__pattern = re.compile(
            fr"""{'|'.join(
                map(
                    lambda x: f'(?P<{x}>{self.__rules[x].compile().pattern})', 
                    self.__rules.keys())
            )}""",
            re.X | re.I
        )

    def __split(self, expression: str) -> list[re.Match, ...]:
        if not self.__pattern:
            self.compile()

        return list(self.__pattern.finditer(expression))

    def __tokenize(self, matches: list[re.Match, ...]) -> list[Token_t, ...]:
        self.__tokens = list(
            map(
                lambda x: next(
                    (c for c in self.__rules[x.lastgroup].group if c.pattern().search(x[x.lastgroup])),
                    AnyChar
                )(x[x.lastgroup], x.start(), x.end()),
                matches
            )
        )
        return self.__tokens
