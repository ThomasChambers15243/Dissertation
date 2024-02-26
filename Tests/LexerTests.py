import unittest
from Code import Lexer


# Tests against an emtpy file
class TestEmpty(unittest.TestCase):
    def test_BlankInput(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/EmtpyFile.py")
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual(operand[0], 0)
        self.assertEqual(len(operand[1]), 0)


# Tests against a file with only comments
class TestOnlyComments(unittest.TestCase):
    def test_OnlyComments(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyComments.py")
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual((operand[0]), 2)
        self.assertEqual(len(operand[1]), 2)


# Tests against a file with only operators,
# Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
class TestOnlyOperators(unittest.TestCase):
    def test_OnlyOperatorsUnique(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyOperators.py")
        self.assertEqual(69, operator[0])
        self.assertEqual(len(operator[1]), 69)


# Tests against a file with only operands,
# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestOnlyOperands(unittest.TestCase):
    def test_OnlyOperandsUnique(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyOperands.py")
        self.assertEqual(44, operand[0])
        self.assertEqual(22, len(operand[1]))


# Tests against a example python scripts
class TestExampleScripts(unittest.TestCase):
    def test_script_1(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript1.py")
        operatorDict = {'=': '=', '(': '(', ')': ')'}
        operandDict = {'a': 'a', '0': '0', 'b': 'b', '10': '10', 'print': 'print', 'Worked': 'Worked'}
        self.assertEqual(4, operator[0])
        self.assertEqual(6, operand[0])
        self.assertEqual(operatorDict, operator[1])
        self.assertEqual(operandDict, operand[1])

    def testScript_2(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript2.py")
        operatorDict = {'def': 'def', '(': '(', ':': ':', ')': ')', '->': '->', 'return': 'return',
                        'for': 'for', 'in': 'in', 'if': 'if', '!=': '!='}
        operandDict = {'Q1': 'Q1', 's': 's', 'str': 'str', 'int': 'int', 'sum': 'sum', 'ord': 'ord',
                       'char': 'char', ' ': ' '}
        self.assertEqual(15, operator[0])
        self.assertEqual(11, operand[0])
        self.assertEqual(operatorDict, operator[1])
        self.assertEqual(operandDict, operand[1])

    def testsScript_3(self):
        lexer = Lexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript3.py")
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

        self.assertEqual(107,operator[0])
        self.assertEqual(82, operand[0])
        self.assertEqual(operatorDict, operator[1])
        self.assertEqual(operandDict, operand[1])



def runTests():
    '''
    Runs all the tests in this file
    '''
    Suite_DB = unittest.TestLoader().loadTestsFromTestCase(TestEmpty)
    Suite_DB.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperators))
    Suite_DB.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyOperands))
    Suite_DB.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlyComments))
    Suite_DB.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExampleScripts))
    return unittest.TextTestRunner().run(Suite_DB)
