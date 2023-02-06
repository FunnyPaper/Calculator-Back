import math
import unittest
from setup import *
from logic import Tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self) -> None:
        self.tokenizer = Tokenizer()

    def test_parse_simple(self):
        self.tokenizer.set_rules(
            number=number,
            b_operator=b_operator
        )
        tokens = [
            Number, BinaryPlus, Number, BinaryMinus, Number,
            BinaryDivide, Number, BinaryMultiply, Number, BinaryModulo, Number
        ]
        self.assertEqual(self.tokenizer.parse("2+4-5/6*1%2"), self.tokenizer.tokens)
        self.assertEqual(len(tokens), len(self.tokenizer.tokens))

        for i, t in enumerate(self.tokenizer.tokens):
            self.assertEqual(type(t), tokens[i])

    def test_parse_unary(self):
        self.tokenizer.set_rules(
            number=number,
            ul_operator=ul_operator,
            ul_start_operator=ul_start_operator,
            b_operator=b_operator
        )
        tokens = [Number, BinaryMinus, UnaryMinus, UnaryMinus, Number]
        self.assertEqual(self.tokenizer.parse("3---2"), self.tokenizer.tokens)
        self.assertEqual(len(tokens), len(self.tokenizer.tokens))

        for i, t in enumerate(self.tokenizer.tokens):
            self.assertEqual(type(t), tokens[i])

    def test_parse_number(self):
        self.tokenizer.set_rules(
            number=number,
        )

        self.assertEqual(list(map(type, self.tokenizer.parse("3"))), [Number])

    def test_parse_constant(self):
        self.tokenizer.set_rules(
            number=constant,
        )

        self.assertEqual(list(map(type, self.tokenizer.parse("pi"))), [PIConstant])
        self.assertEqual(list(map(type, self.tokenizer.parse("e"))), [EConstant])

    def test_parse_function(self):
        self.tokenizer.set_rules(
            function=function,
        )

        self.assertEqual(list(map(type, self.tokenizer.parse("add("))), [FunctionAdd, AnyChar])

    def test_parse_bracket(self):
        self.tokenizer.set_rules(
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
            b_operator=b_operator,
        )

        self.assertEqual(
            list(map(type, self.tokenizer.parse("(2+4)"))),
            [OpenBracket, Number, BinaryPlus, Number, CloseBracket]
        )

    def test_compile(self):
        self.tokenizer.set_rules(
            constant=constant,
            ur_operator=ur_operator
        )
        self.assertEqual(self.tokenizer._Tokenizer__pattern, None)
        self.tokenizer.compile()
        rules = {
            "constant": constant,
            "ur_operator": ur_operator,
            "invalid": Ruleset([AnyChar]),
        }
        pattern = re.compile(
            fr"""{'|'.join(
                map(
                    lambda x: f'(?P<{x}>{rules[x].regex.pattern})', 
                    rules.keys())
            )}""",
            re.X | re.I
        )
        self.assertEqual(self.tokenizer._Tokenizer__pattern.pattern, pattern.pattern)

    def test_set_validator_error(self):
        self.assertRaises(ValueError, self.tokenizer.set_validators, a=2)
        self.assertRaises(ValueError, self.tokenizer.set_validators, b=Number('3', 0, 0))
        self.assertEqual(self.tokenizer.set_validators(c=lambda x: None), None)

    def test_set_rules_error(self):
        self.assertRaises(ValueError, self.tokenizer.set_rules, a=2)
        self.assertRaises(ValueError, self.tokenizer.set_rules, b=Number('3', 0, 0))
        self.assertEqual(self.tokenizer.set_rules(c=separator), None)
