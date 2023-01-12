from logic.tokens.primitive_tokens import *


def verify_groups(tokens: list[Token_t]):
    invalid = next(filter(lambda x: isinstance(x, AnyChar), tokens), None)
    if invalid is not None:
        raise ValueError('Invalid expression', invalid)


def verify_functions(tokens: list[Token_t]):
    separators = []
    while len(tokens) > 0:
        element = tokens.pop()
        if isinstance(element, CloseBracket):
            verify_functions(tokens)
        elif isinstance(element, BinaryComma):
            separators.append(element)
        elif isinstance(element, OpenBracket):
            fun = tokens.pop() if len(tokens) > 0 else None
            length = len(separators)
            if not isinstance(fun, Function) and length > 0:
                raise ValueError('Separators outside function body', separators, fun)
            elif length > 0:
                a_min, a_max = fun.args_min_max
                a_min -= 1
                a_max -= 1
                if not (a_min <= length <= a_max):
                    raise ValueError(
                        fr'Invalid number of separators. Expected {a_min}-{a_max}. Got {length}', separators
                    )
            separators.clear()
