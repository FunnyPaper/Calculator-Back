import math
import unittest
from setup import *
from logic.errors import *

unittest.TestLoader.sortTestMethodsUsing = None


class TestCalculatorGeneral(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_evaluate_simple(self):
        self.calculator.set_rules(
            number=number,
            b_operator=b_operator,
        )
        self.assertEqual(self.calculator.evaluate("4*5+8%4", True), 20)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_empty(self):
        self.assertEqual(self.calculator.evaluate("", True), 0)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_single_number(self):
        self.calculator.set_rules(
            number=number,
        )
        self.assertEqual(self.calculator.evaluate("2.3", True), 2.3)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_invalid_argument(self):
        self.assertRaises(TypeError, self.calculator.evaluate, 5)
        self.assertRaises(TypeError, self.calculator.evaluate, 5+4j)
        self.assertRaises(TypeError, self.calculator.evaluate, [])

    def test_evaluate_invalid_expression(self):
        self.assertRaises(UnrecognizedTokenException, self.calculator.evaluate, "token")
        self.calculator.set_validators(
            group=verify_groups,
        )
        self.assertRaises(UnrecognizedTokenException, self.calculator.evaluate, "token")
        self.assertRaises(UnrecognizedTokenException, self.calculator.evaluate, ")-8-(")

    def test_evaluate_with_brackets(self):
        self.calculator.set_rules(
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
            ul_operator=ul_operator,
            ul_start_operator=ul_start_operator,
            b_operator=b_operator,
        )
        self.assertEqual(self.calculator.evaluate("(2 - (-5/2) * 4)^2"), 144)

    def test_evaluate_pi_constant(self):
        self.calculator.set_rules(
            constant=constant,
        )
        self.assertEqual(self.calculator.evaluate("pi"), math.pi)

    def test_evaluate_e_constant(self):
        self.calculator.set_rules(
            constant=constant,
        )
        self.assertEqual(self.calculator.evaluate("e"), math.e)
