import math
import unittest
from setup import *
from logic import Ruleset


class TestRuleset(unittest.TestCase):

    def test_sort(self):
        self.ruleset = Ruleset([EConstant, PIConstant], sort=True)
        self.assertEqual(self.ruleset.identity, [PIConstant, EConstant])

        self.ruleset = Ruleset([EConstant, PIConstant], sort=False)
        self.assertEqual(self.ruleset.identity, [EConstant, PIConstant])

    def test_regex(self):
        self.ruleset = Ruleset([PIConstant], before=[FunctionAdd], after=[FunctionDivide])
        self.assertEqual(self.ruleset.regex.pattern, "(?<=ADD)(PI)(?=DIV)")

        self.ruleset = Ruleset(
            [PIConstant, EConstant],
            before=[FunctionAdd, FunctionDivide],
            after=[FunctionDivide, FunctionAdd]
        )
        self.assertEqual(self.ruleset.regex.pattern, "(?<=ADD|DIV)(PI|E)(?=DIV|ADD)")

    def test_empty_ruleset(self):
        self.assertRaises(ValueError, Ruleset, [])
