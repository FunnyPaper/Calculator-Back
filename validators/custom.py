from logic.tokens import *
from logic.errors import *


def verify_groups(tokens: list[Token_t]) -> None:
    """
    Verifies if given token list consists of AnyChar (invalid state)

    :param tokens: List of tokens
    """
    invalid = next(filter(lambda x: isinstance(x, AnyChar), tokens), None)
    if invalid is not None:
        raise UnrecognizedTokenException('Invalid expression', invalid)


def verify_functions(tokens: list[Token_t]) -> None:
    """
    Verifies if given token list contains balanced parenthesis
    (and if every function is given appropriate number of arguments)

    :param tokens: List of tokens
    """
    separators = []
    while len(tokens) > 0:
        # Go to next element
        element = tokens.pop()
        if isinstance(element, CloseBracket):
            # In recurrence manner start scope for new bracket pair
            verify_functions(tokens)
        elif isinstance(element, BinaryComma):
            # Append comma to list of separators
            # (could be used as information where invalid separators has been located)
            separators.append(element)
        elif isinstance(element, OpenBracket):
            # Check if separators only occur inside function body (function token is right behind open bracket)
            fun = tokens.pop() if len(tokens) > 0 else None
            length = len(separators)
            if not isinstance(fun, Function) and length > 0:
                raise SeparatorException('Separators outside function body', separators, fun)
            elif isinstance(fun, Function):
                # Get function minimum and maximum number of arguments
                a_min, a_max = fun.args_min_max
                a_min -= 1
                a_max -= 1
                # Raise and error if counted arguments exceed function arguments limit
                if not (a_min <= length <= a_max):
                    raise SeparatorException(
                        fr'Invalid number of separators. Expected {a_min}-{a_max}. Got {length}', separators
                    )

            # Return as current bracket group has been proved to be valid
            return

    # Raise an error as at this point separators are outside any bracket group
    if len(separators) > 0:
        raise SeparatorException('Separators outside bracket group', separators)
