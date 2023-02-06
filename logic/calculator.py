from . import tokenizer
from typing import Callable
import collections.abc
from .tokens import *
from .errors import *


class Calculator:
    """
    Abstracts calculator functionality
    """
    __tokenizer: tokenizer.Tokenizer
    __history: list[dict[str, str]]

    def __init__(self):
        """
        Creates new Calculator
        """
        self.__tokenizer = tokenizer.Tokenizer()
        self.__history = []

    @property
    def history(self) -> list[dict[str, str]]:
        """
        Operations history

        :return: History of operations (lower index represents newer result)
        """
        return self.__history

    def set_rules(self, **kwargs: tokenizer.Ruleset) -> None:
        """
        Sets ruleset for parsing logic

        :param kwargs: Named rulesets (names are used for exception handling)
        """
        self.__tokenizer.set_rules(**kwargs)
        self.__tokenizer.compile()

    def set_validators(self, **validators: Callable[[list[Token_t]], None]) -> None:
        """
        Sets validators for additional checks (they are ignored here)

        :param validators: Callables (called in verify stage of parsing)
        """
        self.__tokenizer.set_validators(**validators)

    def evaluate(self, expression: str, save: bool = False, **operation_options: Union[bool, str]) -> float:
        """
        Evaluates stringified mathematical expression

        :param expression: Stringified mathematical expression
        :param save: Decides if result are added to history
        :param operation_options: Additional options passed to individual math operations
        (ex rad=True for trigonometric functions)
        :return: Result of the equation
        """
        # Enforce that expression is a str
        if not isinstance(expression, str):
            raise TypeError(f"Invalid type: {expression.__class__}. Only strings are allowed.")

        # Internal evaluation stages
        # 1. Parse to token list
        # 2. Convert token list to rpn order
        # 3. Evaluate rpn ordered list
        # 4. Round for precision lost
        tokens: list[Token_t] = self.__tokenizer.parse(expression)
        rpn: list[Token_t] = self.__to_rpn(tokens)
        result: float = round(self.__evaluate_rpn(rpn, **operation_options), 15)

        # Optional saving
        if save:
            # Trim leading 0 in floats such that ex 1.0 becomes 1 but 1.02 is still 1.02
            # (for readability)
            stringified_result: str = re.sub('.0$', '', str(result))
            self.__history.insert(0, {'expression': expression, 'result': stringified_result})

        return result

    def __to_rpn(self, tokens: list[Token_t]) -> list[Token_t]:
        """
        Change given list of tokens order to represent rpn

        :return: Rpn ordered list of tokens
        """
        operators: list[Operator_T] = []
        result: list[Token_t] = []
        for token in tokens:
            # For every token determine if it's operand, operator or special token (such as bracket)
            if issubclass(type(token), Operand):
                # Every operand is appended to result stack
                result.append(token)

            elif issubclass(type(token), OpenBracket):
                # Every opening bracket is forwarded to operators stack
                operators.append(token)

            elif issubclass(type(token), CloseBracket):
                # If given token is closing bracket then
                while not issubclass(type(operators[-1]), OpenBracket):
                    # append every operator token to result stack as long as it's not an open bracket
                    result.append(operators.pop())
                else:
                    # discard operator (it should be an opening bracket)
                    operators.pop()

            elif issubclass(type(token), Operator):
                # In case of operator determine how many (if any) operators should be forwarded to result stack
                # Things to consider are operator precedence, and it's associativity
                while (len(operators) > 0 and not issubclass(type(operators[-1]), OpenBracket) and
                       (operators[-1].precedence > token.precedence or
                       (operators[-1].precedence == token.precedence and
                        token.associativity == Associativity.LTR))):
                    result.append(operators.pop())

                # No matter what given token should still be added to result stack
                # (after optional operators stated earlier)
                operators.append(token)
            else:
                # In any other case given token is completely unrecognized by calculator
                raise UnrecognizedTokenException(f"Invalid token {token}")
        else:
            # Remaining operators goes to the end of rpn
            while len(operators) > 0:
                result.append(operators.pop())

        return result

    def __evaluate_rpn(self, rpn: list[Token_t], **options: Union[bool, str]) -> float:
        """
        Evaluates given list of tokens in rpn order

        :param rpn: List of tokens in rpn order
        :param options: Options to pass to modify operators functionality
        :return: Result of all executed operations
        """
        numbers: list[Union[float, list[float]]] = []
        for token in rpn:
            # For every token try one of possible token case
            try:
                if issubclass(type(token), Operand):
                    # Operands are cast by calling their cast method and appended to numbers stack
                    numbers.append(token.cast)
                elif issubclass(type(token), Binary):
                    # Binary operators expects two arguments
                    # After extraction token operation is executed on given operands
                    # Then result is appended to numbers stack
                    args, numbers = numbers[-2:], numbers[:-2]
                    numbers.append(token.operation(args, **options))
                elif issubclass(type(token), (Unary, Function)):
                    # Unary operators and functions takes single argument as parameter
                    # Said argument needs to be flattened (in case of nesting lists produced by binary comma operator)
                    numbers.append(token.operation(self.__flatten(numbers.pop()), **options))
            except Exception:
                # This stage should be inaccessible
                # (otherwise something went wrong stage earlier or operators were misinterpreted)
                raise CalculationException(f"Unexpected error. Evaluation failed on token {token}")

        return numbers[0] if len(numbers) > 0 else 0.0

    def __flatten(self, x) -> list:
        """
        Flattens given object to one dimensional list

        :param x: object to flatten
        :return: one dimensional list
        """
        if isinstance(x, collections.abc.Iterable):
            return [j for i in x for j in self.__flatten(i)]
        else:
            return [x]
