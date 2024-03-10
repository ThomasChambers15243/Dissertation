import unittest
from config import PATHS
from Code import Lexer

# File Test Name
TEST_NAME = "Lexer"

class TestEmpty(unittest.TestCase):
    """
    Tests against an empty file
    """
    def test_BlankInput(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py")

        self.assertEqual(len(distinct_operator), 0)
        self.assertEqual(len(distinct_operand), 0)

        self.assertEqual(operator_count, 0)
        self.assertEqual(operator_count, 0)


class TestOnlyComments(unittest.TestCase):
    """
    Tests against only comments
    """
    def test_OnlyComments(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py")

        self.assertEqual(len(distinct_operator), 0)
        self.assertEqual(len(distinct_operand), 2)

        self.assertEqual(operator_count, 0)
        self.assertEqual(operand_count, 2)


class TestOnlyOperators(unittest.TestCase):
    """
    Tests against a file with only operators,
    Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
    """
    def test_OnlyOperatorsUnique(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyOperators.py")

        self.assertEqual(69, operator_count)
        self.assertEqual(len(distinct_operator), 69)


class TestOnlyOperands(unittest.TestCase):
    """
    Tests against a file with only operands,
    Operands are variables, methods, constants (False, True, strings and other data type values)
    """
    def test_OnlyOperandsUnique(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyOperands.py")

        self.assertEqual(44, operand_count)
        self.assertEqual(22, len(distinct_operand))



class TestExampleScripts(unittest.TestCase):
    """
    Tests lexer against example python code
    """
    def testScript_1(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py")

        operator_dict = {'=': '=', '(': '(', ')': ')'}
        operand_dict = {'a': 'a', '0': '0', 'b': 'b', '10': '10', 'print': 'print', 'Worked': 'Worked'}

        self.assertEqual(4, operator_count)
        self.assertEqual(6, operand_count)

        self.assertEqual(operator_dict, distinct_operator)
        self.assertEqual(operand_dict, distinct_operand)

    def testScript_2(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript2.py")

        operator_dict = {'def': 'def', '(': '(', ':': ':', ')': ')', '->': '->', 'return': 'return',
                        'for': 'for', 'in': 'in', 'if': 'if', '!=': '!='}

        operand_dict = {'Q1': 'Q1', 's': 's', 'str': 'str', 'int': 'int', 'sum': 'sum', 'ord': 'ord',
                       'char': 'char', ' ': ' '}

        self.assertEqual(15, operator_count)
        self.assertEqual(11, operand_count)

        self.assertEqual(operator_dict, distinct_operator)
        self.assertEqual(operand_dict, distinct_operand)

    def testsScript_3(self):
        lexer = Lexer.Lexer()
        distinct_operator, distinct_operand, operator_count, operand_count = lexer.tokenize_code(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript3.py")

        operator_dict = {'class': 'class', '(': '(', ')': ')', ':': ':', 'def': 'def', '=': '=', '-': '-', '.': '.',
                        '[': '[', ']': ']', 'for': 'for', 'in': 'in', '->': '->', 'if': 'if', '==': '==',
                        'return': 'return', 'while': 'while', '>': '>', '+=': '+='}

        operand_dict = {'Node': 'Node', '__init__': '__init__', 'self': 'self', 'data': 'data', '1': '1',
                        'children': 'children', 'AddChild': 'AddChild', 'node': 'node', 'append': 'append',
                        'AddChildren': 'AddChildren', 'numChildren': 'numChildren', 'int': 'int',
                        'childrenData': 'childrenData', 'list': 'list', 'child': 'child', 'range': 'range',
                        'Q5': 'Q5', 'root': 'root', 'len': 'len', '0': '0', 'foundValues': 'foundValues',
                        'searchStack': 'searchStack', 'currentNode': 'currentNode', 'pop': 'pop', 'set': 'set',
                        'newRoot': 'newRoot', 'i': 'i'}

        self.assertEqual(107, operator_count)
        self.assertEqual(82, operand_count)

        self.assertEqual(operator_dict, distinct_operator)
        self.assertEqual(operand_dict, distinct_operand)


def run_tests():
    """
    Runs all the tests in this file
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmpty)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperators))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperands))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyComments))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExampleScripts))

    return unittest.TextTestRunner().run(suite)
