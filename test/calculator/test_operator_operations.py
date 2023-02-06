import unittest
from setup import *


class TestCalculatorOperatorOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_validators(
            group=verify_groups
        )
        self.calculator.set_rules(
            number=number,
            ul_operator=ul_operator,
            ul_start_operator=ul_start_operator,
            b_operator=b_operator,
            ur_operator=ur_operator
        )

    def test_sum(self):
        self.assertEqual(self.calculator.evaluate("1+1"), 2)

    def test_diff(self):
        self.assertEqual(self.calculator.evaluate("5-3"), 2)

    def test_mul(self):
        self.assertEqual(self.calculator.evaluate("2*5"), 10)

    def test_div(self):
        self.assertEqual(self.calculator.evaluate("10/4"), 2.5)

    def test_modulo(self):
        self.assertEqual(self.calculator.evaluate("11%3"), 2)

    def test_negation(self):
        self.assertEqual(self.calculator.evaluate("-2"), -2)

    def test_factorial(self):
        self.assertEqual(self.calculator.evaluate("5!"), 120)

    def test_power(self):
        self.assertEqual(self.calculator.evaluate("3^4"), 81)

    def test_double_unary_left(self):
        self.assertEqual(self.calculator.evaluate("--3"), 3)

    def test_double_unary_right(self):
        self.assertEqual(self.calculator.evaluate("3!!"), 720)

    def test_double_binary(self):
        self.assertRaises(UnrecognizedTokenException, self.calculator.evaluate, "2/+7")
