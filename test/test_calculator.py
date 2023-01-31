import math
import unittest
from setup import *

unittest.TestLoader.sortTestMethodsUsing = None


class TestCalculatorGeneral(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_validators(
            verify_groups,
            verify_functions
        )
        self.calculator.set_rules(
            function=function,
            separator=separator,
            constant=constant,
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
            ul_operator=ul_operator,
            ul_start_operator=ul_start_operator,
            b_operator=b_operator,
            ur_operator=ur_operator
        )

    def test_evaluate_simple(self):
        self.assertEqual(self.calculator.evaluate("4*5+8%4", True), 20)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_empty(self):
        self.assertEqual(self.calculator.evaluate("", True), 0)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_single_number(self):
        self.assertEqual(self.calculator.evaluate("2.3", True), 2.3)
        self.assertNotEqual(len(self.calculator.history), 0)

    def test_evaluate_invalid_argument(self):
        self.assertRaises(TypeError, self.calculator.evaluate, 5)
        self.assertRaises(TypeError, self.calculator.evaluate, 5+4j)
        self.assertRaises(TypeError, self.calculator.evaluate, [])

    def test_evaluate_invalid_expression(self):
        self.assertRaises(ValueError, self.calculator.evaluate, "token")
        self.assertRaises(ValueError, self.calculator.evaluate, ")-8-(")

    def test_evaluate_with_brackets(self):
        self.assertEqual(self.calculator.evaluate("(2-(-5/2)*4)^2"), 144)

    def test_evaluate_pi_constant(self):
        self.assertEqual(self.calculator.evaluate("pi"), math.pi)

    def test_evaluate_e_constant(self):
        self.assertEqual(self.calculator.evaluate("e"), math.e)


class TestCalculatorOperatorOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
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

    def test_double_negation(self):
        self.assertEqual(self.calculator.evaluate("--3"), 3)

    def test_factorial(self):
        self.assertEqual(self.calculator.evaluate("5!"), 120)

    def test_double_factorial(self):
        self.assertEqual(self.calculator.evaluate("3!!"), 720)

    def test_power(self):
        self.assertEqual(self.calculator.evaluate("3^4"), 81)


class TestCalculatorFunctionOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_rules(
            function=function,
            separator=separator,
            constant=constant,
            open_bracket=open_bracket,
            close_bracket=close_bracket,
            number=number,
        )

    def test_sum(self):
        self.assertEqual(self.calculator.evaluate("add(8,7)"), 15)

    def test_diff(self):
        self.assertEqual(self.calculator.evaluate("sub(6,2,1)"), 3)

    def test_mul(self):
        self.assertEqual(self.calculator.evaluate("mul(2,5)"), 10)

    def test_div(self):
        self.assertEqual(self.calculator.evaluate("div(10,4)"), 2.5)

    def test_floor_div(self):
        self.assertEqual(self.calculator.evaluate("fdiv(10,4)"), 2)

    def test_modulo(self):
        self.assertEqual(self.calculator.evaluate("mod(11,3)"), 2)

    def test_power(self):
        self.assertEqual(self.calculator.evaluate("pow(3,4)"), 81)

    def test_root(self):
        self.assertEqual(self.calculator.evaluate("root(16,4)"), 2)

    def test_min(self):
        self.assertEqual(self.calculator.evaluate("min(2.4,7)"), 2.4)

    def test_max(self):
        self.assertEqual(self.calculator.evaluate("max(2.4,7,999)"), 999)

    def test_log(self):
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


class TestCalculatorValidators(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.set_validators(
            verify_groups,
            verify_functions
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


if __name__ == '__main__':
    unittest.main()
