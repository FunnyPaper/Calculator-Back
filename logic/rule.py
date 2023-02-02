import re
from typing import Type
from .tokens import Token_t


class Ruleset:
    """
    Class abstracting regex construction
    """
    __identity: list[Type[Token_t]]
    __before: list[Type[Token_t]]
    __after: list[Type[Token_t]]

    def __init__(self, identity: list[Type[Token_t]],
                 *,
                 before: list[Type[Token_t]] = None,
                 after: list[Type[Token_t]] = None,
                 sort: bool = True):
        """
        Constructs new Ruleset

        :param identity: Search phrase inside regex ex "[0-4]+"
        :param before: Regex lookbehind ex "(?<=.)" - is not retrieved as a part of a result
        :param after: Regex lookahead ex "(?=.)" - is not retrieved as a part of a result
        :param sort: Decides if passed identity should be sorted
        """
        # Ruleset must define something otherwise regex could become empty string
        if len(identity) == 0:
            raise ValueError("Rule cannot be empty")

        # Initiate fields
        self.enclose(before=before, after=after)

        if sort:
            # Resolve longer tokens first (for similar tokens pattern - ex FDIV and DIV)
            self.__identity = sorted(identity, key=lambda g: len(g.identity().pattern), reverse=True)
        else:
            self.__identity = identity

    @property
    def identity(self) -> list[Type[Token_t]]:
        """
        Ruleset identity (search phrase between lookahead and lookbehind)

        :return: List of token types defining identity
        """
        return self.__identity

    def enclose(self, *, before: list[Type[Token_t]] = None, after: list[Type[Token_t]] = None) -> None:
        """
        Surround the identity with regex lookbehind and/ or lookahead

        :param before: Regex lookbehind ex "(?<=.)"
        :param after: Regex lookahead ex "(?=.)"
        """
        self.__before = before or []
        self.__after = after or []

    @property
    def regex(self) -> re.Pattern:
        """
        Compiles ruleset (by joining identity, before and after lists)

        :return: Ruleset regex pattern object
        """
        # Join lookbehind if before list is not empty
        before = '|'.join(map(lambda x: x.identity().pattern, self.__before))
        if len(before) > 0:
            before = fr"(?<={before})"

        # Join lookahead if after list is not empty
        after = '|'.join(map(lambda x: x.identity().pattern, self.__after))
        if len(after) > 0:
            after = fr"(?={after})"

        # Join identity list
        identity = '|'.join(map(lambda x: x.identity().pattern, self.__identity))

        # Compile pattern object
        return re.compile(fr"{before}({identity}){after}", re.I)
