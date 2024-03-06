import unittest
from config import PATHS
from Code import Lexer


# Tests against an emtpy file
class TestEmpty(unittest.TestCase):
    def test_BlankInput(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py")

        self.assertEqual(len(distinctOperator), 0)
        self.assertEqual(len(distinctOperand), 0)

        self.assertEqual(operatorCount, 0)
        self.assertEqual(operatorCount, 0)


# Tests against a file with only comments
class TestOnlyComments(unittest.TestCase):
    def test_OnlyComments(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py")

        self.assertEqual(len(distinctOperator), 0)
        self.assertEqual(len(distinctOperand), 2)

        self.assertEqual(operatorCount, 0)
        self.assertEqual(operandCount, 2)


# Tests against a file with only operators,
# Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
class TestOnlyOperators(unittest.TestCase):
    def test_OnlyOperatorsUnique(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyOperators.py")

        self.assertEqual(69, operatorCount)
        self.assertEqual(len(distinctOperator), 69)


# Tests against a file with only operands,
# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestOnlyOperands(unittest.TestCase):
    def test_OnlyOperandsUnique(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyOperands.py")

        self.assertEqual(44, operandCount)
        self.assertEqual(22, len(distinctOperand))


# Tests against a example python scripts
class TestExampleScripts(unittest.TestCase):
    def testScript_1(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py")

        operatorDict = {'=': '=', '(': '(', ')': ')'}
        operandDict = {'a': 'a', '0': '0', 'b': 'b', '10': '10', 'print': 'print', 'Worked': 'Worked'}

        self.assertEqual(4, operatorCount)
        self.assertEqual(6, operandCount)

        self.assertEqual(operatorDict, distinctOperator)
        self.assertEqual(operandDict, distinctOperand)

    def testScript_2(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript2.py")

        operatorDict = {'def': 'def', '(': '(', ':': ':', ')': ')', '->': '->', 'return': 'return',
                        'for': 'for', 'in': 'in', 'if': 'if', '!=': '!='}

        operandDict = {'Q1': 'Q1', 's': 's', 'str': 'str', 'int': 'int', 'sum': 'sum', 'ord': 'ord',
                       'char': 'char', ' ': ' '}

        self.assertEqual(15, operatorCount)
        self.assertEqual(11, operandCount)

        self.assertEqual(operatorDict, distinctOperator)
        self.assertEqual(operandDict, distinctOperand)

    def testsScript_3(self):
        lexer = Lexer.Lexer()
        distinctOperator, distinctOperand, operatorCount, operandCount = lexer.TokenizeCode(
            f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript3.py")

        operatorDict = {'class': 'class', '(': '(', ')': ')', ':': ':', 'def': 'def', '=': '=', '-': '-', '.': '.',
                        '[': '[', ']': ']', 'for': 'for', 'in': 'in', '->': '->', 'if': 'if', '==': '==',
                        'return': 'return', 'while': 'while', '>': '>', '+=': '+='}

        operandDict = {'Node': 'Node', '__init__': '__init__', 'self': 'self', 'data': 'data', '1': '1',
                        'children': 'children', 'AddChild': 'AddChild', 'node': 'node', 'append': 'append',
                        'AddChildren': 'AddChildren', 'numChildren': 'numChildren', 'int': 'int',
                        'childrenData': 'childrenData', 'list': 'list', 'child': 'child', 'range': 'range',
                        'Q5': 'Q5', 'root': 'root', 'len': 'len', '0': '0', 'foundValues': 'foundValues',
                        'searchStack': 'searchStack', 'currentNode': 'currentNode', 'pop': 'pop', 'set': 'set',
                        'newRoot': 'newRoot', 'i': 'i'}

        self.assertEqual(107, operatorCount)
        self.assertEqual(82, operandCount)

        self.assertEqual(operatorDict, distinctOperator)
        self.assertEqual(operandDict, distinctOperand)


def runTests():
    """
    Runs all the tests in this file
    """
    Suite = unittest.TestLoader().loadTestsFromTestCase(TestEmpty)
    Suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperators))
    Suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperands))
    Suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyComments))
    Suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExampleScripts))

    return unittest.TextTestRunner().run(Suite)
