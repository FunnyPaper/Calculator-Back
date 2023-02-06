import unittest
from setup import *


class TestCalculatorFunctionOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_validators(
            group=verify_groups,
            function=verify_functions
        )
        self.calculator.set_rules(
            function=function,
            separator=separator,
            constant=constant,
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
        )

    def test_sum_two_arg(self):
        self.assertEqual(self.calculator.evaluate("add(8,7)"), 15)

    def test_sum_one_arg(self):
        self.assertEqual(self.calculator.evaluate("add(8)"), 8)

    def test_diff_two_arg(self):
        self.assertEqual(self.calculator.evaluate("sub(6,2)"), 4)

    def test_diff_one_arg(self):
        self.assertEqual(self.calculator.evaluate("sub(6)"), 6)

    def test_mul_two_arg(self):
        self.assertEqual(self.calculator.evaluate("mul(2,5)"), 10)

    def test_mul_one_arg(self):
        self.assertEqual(self.calculator.evaluate("mul(2)"), 2)

    def test_div_two_arg(self):
        self.assertEqual(self.calculator.evaluate("div(10,4)"), 2.5)

    def test_div_one_arg(self):
        self.assertEqual(self.calculator.evaluate("div(10)"), 10)

    def test_floor_div_two_arg(self):
        self.assertEqual(self.calculator.evaluate("fdiv(10,4)"), 2)

    def test_floor_div_one_arg(self):
        self.assertEqual(self.calculator.evaluate("fdiv(10)"), 10)

    def test_modulo_two_arg(self):
        self.assertEqual(self.calculator.evaluate("mod(11,3)"), 2)

    def test_modulo_one_arg(self):
        self.assertEqual(self.calculator.evaluate("mod(11)"), 11)

    def test_power_two_arg(self):
        self.assertEqual(self.calculator.evaluate("pow(3,4)"), 81)

    def test_power_one_arg(self):
        self.assertEqual(self.calculator.evaluate("pow(3)"), 9)

    def test_root_two_arg(self):
        self.assertEqual(self.calculator.evaluate("root(16,4)"), 2)

    def test_root_one_arg(self):
        self.assertEqual(self.calculator.evaluate("root(16)"), 4)

    def test_min_two_arg(self):
        self.assertEqual(self.calculator.evaluate("min(2.4,7)"), 2.4)

    def test_min_one_arg(self):
        self.assertEqual(self.calculator.evaluate("min(2.4)"), 2.4)

    def test_max_two_arg(self):
        self.assertEqual(self.calculator.evaluate("max(7,999)"), 999)

    def test_max_one_arg(self):
        self.assertEqual(self.calculator.evaluate("max(999)"), 999)

    def test_log_two_arg(self):
        self.assertEqual(self.calculator.evaluate("log(81,3)"), 4)

    def test_log10(self):
        self.assertEqual(self.calculator.evaluate("log(100)"), 2)

    def test_ln(self):
        self.assertEqual(self.calculator.evaluate("ln(e)"), 1)

    def test_sin_rad(self):
        self.assertAlmostEqual(self.calculator.evaluate("sin(1)", rad=True), 0.01745240643)

    def test_sin_deg(self):
        self.assertAlmostEqual(self.calculator.evaluate("sin(1)"), 0.8414709848)

    def test_cos_rad(self):
        self.assertAlmostEqual(self.calculator.evaluate("cos(1)", rad=True), 0.99984769515)

    def test_cos_deg(self):
        self.assertAlmostEqual(self.calculator.evaluate("cos(1)"), 0.54030230586)

    def test_tan_rad(self):
        self.assertAlmostEqual(self.calculator.evaluate("tan(1)", rad=True), 0.01745506492)

    def test_tan_deg(self):
        self.assertAlmostEqual(self.calculator.evaluate("tan(1)"), 1.55740772465)
