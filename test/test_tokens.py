import math
import unittest
from setup import *
from logic import Ruleset


class TestTokens(unittest.TestCase):

    def test_binary(self):
        self.assertEqual(BinaryPlus("+", 0, 0).operation([5, 7]), 12)
        self.assertRaises(ValueError, BinaryPlus, 'a', 0, 0)

        self.assertEqual(BinaryMinus("-", 0, 0).operation([5, 7]), -2)
        self.assertRaises(ValueError, BinaryMinus, 'a', 0, 0)

        self.assertEqual(BinaryMultiply("*", 0, 0).operation([5, 7]), 35)
        self.assertRaises(ValueError, BinaryMultiply, 'a', 0, 0)

        self.assertEqual(BinaryDivide("/", 0, 0).operation([5, 10]), 0.5)
        self.assertRaises(ValueError, BinaryDivide, 'a', 0, 0)

        self.assertEqual(BinaryModulo("%", 0, 0).operation([5, 7]), 5)
        self.assertRaises(ValueError, BinaryModulo, 'a', 0, 0)

        self.assertEqual(BinaryComma(",", 0, 0).operation([5, 7]), [5, 7])
        self.assertRaises(ValueError, BinaryComma, 'a', 0, 0)

        self.assertEqual(BinaryExponent("^", 0, 0).operation([2, 3]), 8)
        self.assertRaises(ValueError, BinaryExponent, 'a', 0, 0)

    def test_function(self):
        self.assertEqual(FunctionModulo("mod", 0, 0).operation([120, 111, 5]), 4)
        self.assertEqual(FunctionModulo("mod", 0, 0).operation([2]), 2)
        self.assertRaises(ValueError, FunctionModulo, 'a', 0, 0)

        self.assertEqual(FunctionFloorDivision("fdiv", 0, 0).operation([20, 3, 5]), 1)
        self.assertEqual(FunctionFloorDivision("fdiv", 0, 0).operation([2.4]), 2)
        self.assertRaises(ValueError, FunctionFloorDivision, 'a', 0, 0)

        self.assertEqual(FunctionMin("min", 0, 0).operation([2, 3, 4, 5]), 2)
        self.assertRaises(ValueError, FunctionMin, 'a', 0, 0)

        self.assertEqual(FunctionMax("max", 0, 0).operation([2, 3, 4, 5]), 5)
        self.assertRaises(ValueError, FunctionMax, 'a', 0, 0)

        self.assertEqual(FunctionRoot("root", 0, 0).operation([15625, 3, 2]), 5)
        self.assertEqual(FunctionRoot("root", 0, 0).operation([16]), 4)
        self.assertRaises(ValueError, FunctionRoot, 'a', 0, 0)

        self.assertEqual(FunctionPow("pow", 0, 0).operation([2, 3, 4]), 4096)
        self.assertEqual(FunctionPow("pow", 0, 0).operation([3]), 9)
        self.assertRaises(ValueError, FunctionPow, 'a', 0, 0)

        self.assertEqual(FunctionLog("log", 0, 0).operation([25, 5]), 2)
        self.assertEqual(FunctionLog("log", 0, 0).operation([1000]), 3)
        self.assertRaises(ValueError, FunctionLog, 'a', 0, 0)

        self.assertEqual(FunctionAdd("add", 0, 0).operation([2, 3, 4, 5]), 14)
        self.assertEqual(FunctionAdd("add", 0, 0).operation([2]), 2)
        self.assertRaises(ValueError, FunctionAdd, 'a', 0, 0)

        self.assertEqual(FunctionSubtract("sub", 0, 0).operation([2, 3, 4, 5]), -10)
        self.assertEqual(FunctionSubtract("sub", 0, 0).operation([2]), 2)
        self.assertRaises(ValueError, FunctionSubtract, 'a', 0, 0)

        self.assertEqual(FunctionMultiply("mul", 0, 0).operation([2, 3, 4, 5]), 120)
        self.assertEqual(FunctionMultiply("mul", 0, 0).operation([2]), 2)
        self.assertRaises(ValueError, FunctionMultiply, 'a', 0, 0)

        self.assertEqual(FunctionDivide("div", 0, 0).operation([5, 4, 2]), 0.625)
        self.assertEqual(FunctionDivide("div", 0, 0).operation([5]), 5)
        self.assertRaises(ValueError, FunctionDivide, 'a', 0, 0)

        self.assertAlmostEqual(FunctionSin("sin", 0, 0).operation([30], rad=True), 0.5, 1)
        self.assertAlmostEqual(FunctionSin("sin", 0, 0).operation([30]), -0.988031624, 8)
        self.assertRaises(ValueError, FunctionSin, 'a', 0, 0)

        self.assertAlmostEqual(FunctionCos("cos", 0, 0).operation([60], rad=True), 0.5, 1)
        self.assertAlmostEqual(FunctionCos("cos", 0, 0).operation([60]), -0.95241298, 8)
        self.assertRaises(ValueError, FunctionCos, 'a', 0, 0)

        self.assertAlmostEqual(FunctionTan("tan", 0, 0).operation([45], rad=True), 1)
        self.assertAlmostEqual(FunctionTan("tan", 0, 0).operation([45]), 1.61977519, 8)
        self.assertRaises(ValueError, FunctionTan, 'a', 0, 0)

        self.assertEqual(FunctionLn("ln", 0, 0).operation([math.e]), 1)
        self.assertRaises(ValueError, FunctionLn, 'a', 0, 0)

    def test_operand(self):
        self.assertEqual(Number("4", 0, 0).cast, 4)
        self.assertRaises(ValueError, Number, 'a', 0, 0)

        self.assertEqual(PIConstant("pi", 0, 0).cast, math.pi)
        self.assertRaises(ValueError, PIConstant, 'a', 0, 0)

        self.assertEqual(EConstant("e", 0, 0).cast, math.e)
        self.assertRaises(ValueError, EConstant, 'a', 0, 0)

    def test_unary(self):
        self.assertEqual(UnaryMinus('-', 0, 0).operation([3]), -3)
        self.assertRaises(ValueError, UnaryMinus, 'a', 0, 0)

        self.assertEqual(UnaryFactorial('!', 0, 0).operation([6]), 720)
        self.assertRaises(ValueError, UnaryFactorial, 'a', 0, 0)

    def test_primitive(self):
        self.assertRaises(ValueError, OpenBracket, 'a', 0, 0)
        self.assertRaises(ValueError, CloseBracket, 'a', 0, 0)
        self.assertRaises(ValueError, EndAnchor, 'a', 0, 0)
        self.assertEqual(StartAnchor("", 0, 0).value, '')
        self.assertEqual(AnyChar("anything", 0, 0).value, 'anything')
