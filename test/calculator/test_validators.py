import math
import unittest
from setup import *


class TestCalculatorValidators(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_validators(
            group=verify_groups,
            function=verify_functions
        )

    def test_anything_is_invalid(self):
        self.assertRaises(ValueError, self.calculator.evaluate, "1+2")
        self.assertRaises(ValueError, self.calculator.evaluate, "3")
        self.assertRaises(ValueError, self.calculator.evaluate, "-1")
        self.assertRaises(ValueError, self.calculator.evaluate, "3^5")
        self.assertRaises(ValueError, self.calculator.evaluate, "Min(Max(4,5),6)")

    def test_invalid_function(self):
        self.calculator.set_rules(
            function=function,
            separator=separator,
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
        )
        self.assertRaises(ValueError, self.calculator.evaluate, "add(2,)")
        self.assertRaises(ValueError, self.calculator.evaluate, "fdiv(,2)")
        self.assertRaises(ValueError, self.calculator.evaluate, "mul(,)")
        self.assertRaises(ValueError, self.calculator.evaluate, "sub()")

    def test_only_included_groups_are_valid(self):
        self.assertRaises(ValueError, self.calculator.evaluate, "2")
        self.calculator.set_rules(
            number=number,
        )
        self.assertEqual(self.calculator.evaluate("2"), 2)
        self.calculator.set_rules(
            function=function,
            separator=separator,
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
        )
        self.assertEqual(self.calculator.evaluate("add(4,5,6)"), 15)
        self.assertRaises(ValueError, self.calculator.evaluate, "4+5+6")
        self.assertRaises(ValueError, self.calculator.evaluate, "e")
        self.calculator.set_rules(
            constant=constant,
            number=number,
            b_operator=b_operator,
        )
        self.assertRaises(ValueError, self.calculator.evaluate, "add(4,5,6)")
        self.assertEqual(self.calculator.evaluate("4+5+6"), 15)
        self.assertEqual(self.calculator.evaluate("e"), math.e)

    def test_separators_outside_function(self):
        self.calculator.set_rules(
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            function=function,
            separator=separator,
            number=number,
            b_operator=b_operator
        )

        self.assertRaises(ValueError, self.calculator.evaluate, "6,7+log(100,2)")
        self.assertRaises(ValueError, self.calculator.evaluate, "6+(100,2)")
        self.assertRaises(ValueError, self.calculator.evaluate, "(100,2)")

    def test_function_arg_limit_exceeded(self):
        self.calculator.set_rules(
            function=function,
            separator=separator,
            number=number
        )

        self.assertRaises(ValueError, self.calculator.evaluate, "sin(7,6)")
        self.assertRaises(ValueError, self.calculator.evaluate, "sin")
