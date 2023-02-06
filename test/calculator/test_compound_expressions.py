import math
import unittest
from setup import *

unittest.TestLoader.sortTestMethodsUsing = None


class TestCalculatorCompoundExpressions(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
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
        self.calculator.set_validators(
            group=verify_groups,
            function=verify_functions
        )

    def test_expression_1(self):
        self.assertEqual(self.calculator.evaluate("2+3-4-5+2+4-8"), -6)

    def test_expression_2(self):
        self.assertEqual(self.calculator.evaluate("3*2/4/2*5/4*6%10"), 5.625)

    def test_expression_3(self):
        self.assertEqual(self.calculator.evaluate("-2+3!^2-3!!"), -686)

    def test_expression_4(self):
        self.assertEqual(self.calculator.evaluate("5*3-5--2/5%2+4^3!"), 4104.4)

    def test_expression_5(self):
        self.assertEqual(self.calculator.evaluate("1+(3-5/2)*(2+4%3)"), 2.5)

    def test_expression_6(self):
        self.assertAlmostEqual(
            self.calculator.evaluate("-(--((((6+5)^(13%11)*2/10)--7+3)*6-3)%5*(2--(5)))*2"), -30.8, 1
        )

    def test_expression_7(self):
        self.assertEqual(self.calculator.evaluate("FDiv(pow(Log(100)*Ln(e),min(MAX(3,e,pi),3.1),3)"), 630)

    def test_expression_8(self):
        self.assertAlmostEqual(self.calculator.evaluate("add(2,5,7)*sin(30)^mUL(2,2,2)", rad=True), 0.0546875, 7)

    def test_expression_9(self):
        self.assertEqual(
            self.calculator.evaluate(
                "fdiv(tan(pi)+(3-sub(min(Pi,e),max(pI,e),sin(2*pi))%2^(3-div(2))),0.3)"), 4
        )

    def test_expression_10(self):
        self.assertRaises(ValueError, self.calculator.evaluate, "3/0")
