from logic import tokenizer
from logic.calculator import Calculator
from validators.custom import *

# Required for Rule objects (and __subclasses__ method)
from logic.tokens import operand_tokens, unary_tokens, binary_tokens, function_tokens
from logic.tokens.primitive_tokens import *

# Rules
function = tokenizer.Rule(Function.__subclasses__())
separator = tokenizer.Rule([BinaryComma])
constant = tokenizer.Rule([*operand_tokens.Constant.__subclasses__()])
open_bracket = tokenizer.Rule([OpenBracket])
close_bracket = tokenizer.Rule([CloseBracket])
number = tokenizer.Rule([operand_tokens.Number])
ul_operator = tokenizer.Rule([*unary_tokens.UnaryLeft.__subclasses__()])
ul_start_operator = tokenizer.Rule([*unary_tokens.UnaryLeft.__subclasses__()])
b_operator = tokenizer.Rule([*Binary.__subclasses__()])
ur_operator = tokenizer.Rule([*unary_tokens.UnaryRight.__subclasses__()])

# Rules before/after restrictions
function.add(after=[*open_bracket.group])
separator.add(
    after=[*ul_operator.group, *number.group, *open_bracket.group, *constant.group, *function.group]
)
constant.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, EndAnchor]
)
open_bracket.add(
    after=[*number.group, *ul_operator.group, *open_bracket.group, *constant.group, *function.group]
)
close_bracket.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, EndAnchor]
)
number.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, EndAnchor]
)
ul_operator.add(
    before=[*b_operator.group, *open_bracket.group, *separator.group],
    after=[*number.group, *ul_operator.group, *open_bracket.group, *function.group, *constant.group]
)
ul_start_operator.add(
    before=[StartAnchor],
    after=[*number.group, *ul_operator.group, *open_bracket.group, *function.group, *constant.group]
)
b_operator.add(
    after=[*ul_operator.group, *number.group, *open_bracket.group, *constant.group, *function.group]
)
ur_operator.add(
    after=[*separator.group, *ur_operator.group, *number.group, *b_operator.group, *close_bracket.group, EndAnchor]
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
    verify_groups,
    verify_functions
)
