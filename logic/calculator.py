import math

from logic import tokenizer
from typing import Union, Callable
import collections.abc
from logic import default_rules


class Calculator:
    __tokenizer: tokenizer.Tokenizer = tokenizer.Tokenizer()
    __history: list[dict[str, str]] = []

    @property
    def history(self):
        return self.__history

    def set_rules(self, **kwargs: tokenizer.Rule):
        self.__tokenizer.set_rules(**kwargs)
        self.__tokenizer.compile()

    def set_validators(self, *validators: Callable[[list[tokenizer.Token_t]], None]):
        self.__tokenizer.set_validators(*validators)

    def evaluate(self, expression: str, save: bool, **operation_options: Union[bool, str]) -> str:
        self.__tokenizer.parse(expression)
        result: str = str(round(self.evaluate_rpn(self.__to_rpn(), **operation_options), 15))
        result = result.replace('.0', '')
        if save:
            self.__history.insert(0, {'expression': expression, 'result': result})

        return result

    def __to_rpn(self) -> list[tokenizer.Token_t]:
        operators: list[tokenizer.Operator_T] = []
        result: list[tokenizer.Token_t] = []
        for token in self.__tokenizer.tokens:
            if issubclass(type(token), tokenizer._Operand):
                result.append(token)
            elif issubclass(type(token), (tokenizer.Function, tokenizer.OpenBracket)):
                operators.append(token)
            elif issubclass(type(token), tokenizer.CloseBracket):
                while not issubclass(type(operators[-1]), tokenizer.OpenBracket):
                    result.append(operators.pop())
                else:
                    operators.pop()

            elif issubclass(type(token), tokenizer._Operator):
                while (len(operators) > 0 and not issubclass(type(operators[-1]), tokenizer.OpenBracket) and
                       (operators[-1].precedence > token.precedence or
                       (operators[-1].precedence == token.precedence and
                        token.associativity == tokenizer._Associativity.LTR))):
                    result.append(operators.pop())

                operators.append(token)
        else:
            # remaining operators goes to the end of rpn
            while len(operators) > 0:
                result.append(operators.pop())

        return result

    def evaluate_rpn(self, rpn: list[tokenizer.Token_t, ...], **options: Union[bool, str]) -> float:
        numbers: list[Union[float, list[float]]] = []
        for token in rpn:
            if issubclass(type(token), tokenizer._Operand):
                numbers.append(token.cast)
            elif issubclass(type(token), tokenizer.Binary):
                args, numbers = numbers[-2:], numbers[:-2]
                numbers.append(token.operation(args, **options))
            elif issubclass(type(token), (tokenizer.Unary, tokenizer.Function)):
                numbers.append(token.operation(self.__flatten(numbers.pop()), **options))

        return numbers[0] if len(numbers) > 0 else 0.0

    def __flatten(self, x):
        if isinstance(x, collections.abc.Iterable):
            return [j for i in x for j in self.__flatten(i)]
        else:
            return [x]


def verify_groups(tokens: list[tokenizer.Token_t]):
    invalid = next(filter(lambda x: isinstance(x, tokenizer.AnyChar), tokens), None)
    if invalid is not None:
        raise ValueError('Invalid expression', invalid)


def verify_functions(tokens: list[tokenizer.Token_t]):
    separators = []
    while len(tokens) > 0:
        element = tokens.pop()
        if isinstance(element, tokenizer.CloseBracket):
            verify_functions(tokens)
        elif isinstance(element, tokenizer.BinaryComma):
            separators.append(element)
        elif isinstance(element, tokenizer.OpenBracket):
            fun = tokens.pop() if len(tokens) > 0 else None
            length = len(separators)
            if not isinstance(fun, tokenizer.Function) and length > 0:
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


if __name__ == "__main__":
    one = '1+2.9-3+-MiN(1*MAX(5,SIN(1)),(PI/8))-(5*TAN(7)/(2-0))+2!-(1-(-2))-(-(-(-(-9))))+PI'
    two = 'Add(Root(256,2,4),Pow(4,2,2,-2),Mul(2,5,6))'
    three = f'min(9,pi,MAX(8,8))'
    four = '-(2)'
    calculator: Calculator = Calculator()
    calculator.set_rules(
        function=default_rules.function,
        separator=default_rules.separator,
        constant=default_rules.constant,
        open_bracket=default_rules.open_bracket,
        close_bracket=default_rules.close_bracket,
        number=default_rules.number,
        # fixed length lookbehind (first for visible symbols, second for string start)
        # - can be unary or binary (so both groups have to be more specific about matching)
        ul_operator=default_rules.ul_operator,
        ul_start_operator=default_rules.ul_start_operator,
        b_operator=default_rules.b_operator,
        ur_operator=default_rules.ur_operator
    )
    calculator.set_validators(
        verify_groups,
        verify_functions
    )
    print(one, '=', calculator.evaluate(one, True))
    print(two, '=', calculator.evaluate(two, True))
    print(three, '=', calculator.evaluate(three, True))
    print(four, '=', calculator.evaluate(four, True))
