import re
from typing import Callable, Iterator
from .tokens import Token_t, AnyChar
from .ruleset import Ruleset


class Tokenizer:
    """
    Class abstracting token parsing
    """
    __rules: dict[str, Ruleset]
    __tokens: list[Token_t]
    __validators: dict[str, Callable[[list[Token_t]], None]]
    __pattern: re.Pattern

    def __init__(self):
        """
        Constructs new Tokenizer
        """

        # Initiate fields
        self.__rules = dict()
        self.__tokens = []
        self.__validators = dict()
        self.__pattern = None

    @property
    def tokens(self) -> list[Token_t]:
        """
        Tokens parsed in last parse operation

        :return: List of parsed tokens
        """
        return self.__tokens

    def set_rules(self, **kwargs: Ruleset) -> None:
        """
        Sets ruleset for parsing logic

        :param kwargs: Named rulesets (names are used for exception handling)
        """
        # Enforce valid type
        for k, v in kwargs.items():
            if not isinstance(v, Ruleset):
                raise ValueError(f"{k} rule must be an instance of {Ruleset} or one of it's subclass", str(v))

        self.__rules = kwargs

    def set_validators(self, **validators: Callable[[list[Token_t]], None]) -> None:
        """
        Sets validators for additional checks (they are ignored here)

        :param validators: Callables (called in verify stage of parsing)
        """
        # Enforce valid type
        for k, v in validators.items():
            if not isinstance(v, Callable):
                raise ValueError(f"{k} validator must be a callable", str(v))

        self.__validators = validators

    def parse(self, expression: str) -> list[Token_t]:
        """
        Parses mathematical expression

        :param expression: Stringified mathematical expression
        :return: List of tokens (tokenized mathematical expression)
        """
        # Internal parsing stages
        # 1. Split expression
        # 2. Tokenize splitted iterable of match objects (tokens if match object format)
        # 3. Verify (call set validators)
        split: Iterator[re.Match] = self.__split(expression)
        tokens: list[Token_t] = self.__tokenize(split)
        self.__verify()

        return tokens

    def compile(self) -> None:
        """
        Compiles rulesets into regex pattern object for further use
        """
        # "invalid" ruleset is reserved for AnyChar (matching entire expression)
        # in case of unrecognized pattern
        self.__rules["invalid"] = Ruleset([AnyChar])
        self.__pattern = re.compile(
            fr"""{'|'.join(
                map(
                    lambda x: f'(?P<{x}>{self.__rules[x].regex.pattern})', 
                    self.__rules.keys())
            )}""",
            re.X | re.I
        )

    def __verify(self) -> None:
        """
        Calls validators in loop passing copy of token list (user shouldn't change parse result)
        """
        for k, v in self.__validators.items():
            v(self.__tokens[:])

    def __split(self, expression: str) -> Iterator[re.Match]:
        """
        Splits stringified mathematical expression into regex match objects (reflected by set rulesets)

        :param expression: Stringified mathematical expression
        :return: List of regex match objects
        """
        # Check if parse pattern is set
        if not self.__pattern:
            self.compile()

        # Extract tokens (as iterable of match objects)
        return self.__pattern.finditer(re.sub(r"\s", '', expression))

    def __tokenize(self, matches: Iterator[re.Match]) -> list[Token_t]:
        """
        Converts iterable of match objects into list of tokens (more readable)

        :param matches: Iterable of match objects
        :return: List of tokens
        """
        # Map every match object into token object by using appropriate constructor
        # Constructors are matched by checking in order identity of named ruleset that created the match in expression
        # Every ruleset contains an identity list of token constructors
        # Regex match is performed by named groups (the same as named ruleset)
        self.__tokens = list(
            map(
                lambda x: next(
                    (c for c in self.__rules[x.lastgroup].identity if c.identity().search(x[x.lastgroup])),
                    AnyChar
                )(x[x.lastgroup], x.start(), x.end()),
                matches
            )
        )
        return self.__tokens
