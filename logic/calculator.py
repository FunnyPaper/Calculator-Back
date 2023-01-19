from . import tokenizer
from typing import Union, Callable
import collections.abc
from .tokens import *


class Calculator:
    __tokenizer: tokenizer.Tokenizer = tokenizer.Tokenizer()
    __history: list[dict[str, str]] = []

    @property
    def history(self):
        return self.__history

    def set_rules(self, **kwargs: tokenizer.Rule):
        self.__tokenizer.set_rules(**kwargs)
        self.__tokenizer.compile()

    def set_validators(self, *validators: Callable[[list[Token_t]], None]):
        self.__tokenizer.set_validators(*validators)

    def evaluate(self, expression: str, save: bool, **operation_options: Union[bool, str]) -> str:
        self.__tokenizer.parse(expression)
        result: str = str(round(self.evaluate_rpn(self.__to_rpn(), **operation_options), 15))
        result = result.replace('.0', '')
        if save:
            self.__history.insert(0, {'expression': expression, 'result': result})

        return result

    def __to_rpn(self) -> list[Token_t]:
        operators: list[Operator_T] = []
        result: list[Token_t] = []
        for token in self.__tokenizer.tokens:
            if issubclass(type(token), Operand):
                result.append(token)
            elif issubclass(type(token), (Function, OpenBracket)):
                operators.append(token)
            elif issubclass(type(token), CloseBracket):
                while not issubclass(type(operators[-1]), OpenBracket):
                    result.append(operators.pop())
                else:
                    operators.pop()

            elif issubclass(type(token), Operator):
                while (len(operators) > 0 and not issubclass(type(operators[-1]), OpenBracket) and
                       (operators[-1].precedence > token.precedence or
                       (operators[-1].precedence == token.precedence and
                        token.associativity == Associativity.LTR))):
                    result.append(operators.pop())

                operators.append(token)
        else:
            # remaining operators goes to the end of rpn
            while len(operators) > 0:
                result.append(operators.pop())

        return result

    def evaluate_rpn(self, rpn: list[Token_t, ...], **options: Union[bool, str]) -> float:
        numbers: list[Union[float, list[float]]] = []
        for token in rpn:
            if issubclass(type(token), Operand):
                numbers.append(token.cast)
            elif issubclass(type(token), Binary):
                args, numbers = numbers[-2:], numbers[:-2]
                numbers.append(token.operation(args, **options))
            elif issubclass(type(token), (Unary, Function)):
                numbers.append(token.operation(self.__flatten(numbers.pop()), **options))

        return numbers[0] if len(numbers) > 0 else 0.0

    def __flatten(self, x):
        if isinstance(x, collections.abc.Iterable):
            return [j for i in x for j in self.__flatten(i)]
        else:
            return [x]
