import re
from collections.abc import Sequence
from typing import Callable
from logic.tokens.primitive_tokens import Token_t, AnyChar


class Rule:
    __group: list[Token_t] = []
    __before: list[Token_t] = []
    __after: list[Token_t] = []

    def __init__(self, group: list[Token_t]):
        if len(group) == 0:
            raise ValueError("Rule cannot be empty")

        # Resolve longer tokens first (for similar tokens pattern - ex FDIV and DIV)
        self.__group = sorted(group, key=lambda g: len(g.pattern().pattern), reverse=True)

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
