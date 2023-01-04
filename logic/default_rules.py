from logic.tokens import operand_tokens, unary_tokens, binary_tokens, function_tokens
from logic import tokenizer

function = tokenizer.Rule(tokenizer.Function.__subclasses__())
separator = tokenizer.Rule([tokenizer.BinaryComma])
constant = tokenizer.Rule([*operand_tokens.Constant.__subclasses__()])
open_bracket = tokenizer.Rule([tokenizer.OpenBracket])
close_bracket = tokenizer.Rule([tokenizer.CloseBracket])
number = tokenizer.Rule([operand_tokens.Number])
ul_operator = tokenizer.Rule([*unary_tokens.UnaryLeft.__subclasses__()])
ul_start_operator = tokenizer.Rule([*unary_tokens.UnaryLeft.__subclasses__()])
b_operator = tokenizer.Rule([*tokenizer.Binary.__subclasses__()])
ur_operator = tokenizer.Rule([*unary_tokens.UnaryRight.__subclasses__()])

function.add(after=[*open_bracket.group])
separator.add(
    after=[*ul_operator.group, *number.group, *open_bracket.group, *constant.group, *function.group]
)
constant.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, tokenizer.EndAnchor]
)
open_bracket.add(
    after=[*number.group, *ul_operator.group, *open_bracket.group, *constant.group, *function.group]
)
close_bracket.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, tokenizer.EndAnchor]
)
number.add(
    after=[*ur_operator.group, *close_bracket.group, *b_operator.group, *separator.group, tokenizer.EndAnchor]
)
ul_operator.add(
    before=[*b_operator.group, *open_bracket.group, *separator.group],
    after=[*number.group, *ul_operator.group, *open_bracket.group, *function.group, *constant.group]
)
ul_start_operator.add(
    before=[tokenizer.StartAnchor],
    after=[*number.group, *ul_operator.group, *open_bracket.group, *function.group, *constant.group]
)
b_operator.add(
    after=[*ul_operator.group, *number.group, *open_bracket.group, *constant.group, *function.group]
)
ur_operator.add(
    after=[*separator.group, *ur_operator.group, *number.group, *b_operator.group, *close_bracket.group, tokenizer.EndAnchor]
)
