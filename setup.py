from logic.ruleset import Ruleset
from logic.calculator import Calculator
from validators import *

# Required for Rule objects (and __subclasses__ method)
from logic.tokens import operand_tokens, unary_tokens, binary_tokens, function_tokens

# Rules
function = Ruleset(Function.__subclasses__())
separator = Ruleset([binary_tokens.BinaryComma])
constant = Ruleset([*operand_tokens.Constant.__subclasses__()])
open_bracket = Ruleset([OpenBracket])
close_bracket = Ruleset([CloseBracket])
number = Ruleset([operand_tokens.Number])
ul_operator = Ruleset([*unary_tokens.UnaryLeft.__subclasses__()])
ul_start_operator = Ruleset([*unary_tokens.UnaryLeft.__subclasses__()])
b_operator = Ruleset([*Binary.__subclasses__()])
ur_operator = Ruleset([*unary_tokens.UnaryRight.__subclasses__()])

# Rules before/after restrictions
function.enclose(after=[*open_bracket.identity])
separator.enclose(
    after=[*ul_operator.identity, *number.identity, *open_bracket.identity, *constant.identity, *function.identity]
)
constant.enclose(
    after=[*ur_operator.identity, *close_bracket.identity, *b_operator.identity, *separator.identity, EndAnchor]
)
open_bracket.enclose(
    after=[*number.identity, *ul_operator.identity, *open_bracket.identity, *constant.identity, *function.identity]
)
close_bracket.enclose(
    after=[*ur_operator.identity, *close_bracket.identity, *b_operator.identity, *separator.identity, EndAnchor]
)
number.enclose(
    after=[*ur_operator.identity, *close_bracket.identity, *b_operator.identity, *separator.identity, EndAnchor]
)
ul_operator.enclose(
    before=[*b_operator.identity, *open_bracket.identity, *separator.identity],
    after=[*number.identity, *ul_operator.identity, *open_bracket.identity, *function.identity, *constant.identity]
)
ul_start_operator.enclose(
    before=[StartAnchor],
    after=[*number.identity, *ul_operator.identity, *open_bracket.identity, *function.identity, *constant.identity]
)
b_operator.enclose(
    after=[*ul_operator.identity, *number.identity, *open_bracket.identity, *constant.identity, *function.identity]
)
ur_operator.enclose(
    after=[*separator.identity, *ur_operator.identity, *number.identity, *b_operator.identity, *close_bracket.identity, EndAnchor]
)

# Calculator object
calculator: Calculator = Calculator()
calculator.set_rules(
    function=function,
    separator=separator,
    constant=constant,
    open_bracket=open_bracket,
    close_bracket=close_bracket,
    number=number,
    # fixed length lookbehind (first for visible symbols, second for string start)
    # - can be unary or binary (so both groups have to be more specific about matching)
    ul_operator=ul_operator,
    ul_start_operator=ul_start_operator,
    b_operator=b_operator,
    ur_operator=ur_operator
)
calculator.set_validators(
    group=verify_groups,
    function=verify_functions
)
