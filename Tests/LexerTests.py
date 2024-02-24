import unittest
from Code import newLexer


# Tests against an emtpy file
class TestEmpty(unittest.TestCase):
    def test_BlankInput(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/EmtpyFile.py")
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual(operand[0], 0)
        self.assertEqual(len(operand[1]), 0)


# Tests against a file with only comments
class TestOnlyComments(unittest.TestCase):
    def test_OnlyComments(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyComments.py")
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual((operand[0]), 2)
        self.assertEqual(len(operand[1]), 2)


# Tests against a file with only operators,
# Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
# Currently fails due to lexer not catching operators such as '+='
# It splits them up into '+' '='
# So higher total count, less unique
class TestOnlyOperators(unittest.TestCase):
    def test_OnlyOperatorsUnique(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyOperators.py")
        self.assertEqual(69, operator[0])
        self.assertEqual(len(operator[1]), 69)


# Tests against a file with only operands,
# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestOnlyOperands(unittest.TestCase):
    def test_OnlyOperandsUnique(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/OnlyOperands.py")
        self.assertEqual(40, operand[0])
        self.assertEqual(20, len(operand[1]))


# Tests against a file with only operands,
# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestExampleScripts(unittest.TestCase):
    def test_script_1(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript1.py")
        operatorDict = {'=': '=', '(': '(', ')': ')'}
        operandDict = {'a': 'a', '0': '0', 'b': 'b', '10': '10', 'print': 'print', 'Worked': 'Worked'}
        self.assertEqual(4, operator[0])
        self.assertEqual(6, operand[0])
        self.assertEqual(operatorDict, operator[1])
        self.assertEqual(operandDict, operand[1])

    def testScript_2(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript2.py")
        operatorDict = {'def': 'def', '(': '(', ':': ':', ')': ')', '->': '->', 'return': 'return',
                        'for': 'for', 'in': 'in', 'if': 'if', '!=': '!='}
        operandDict = {'Q1': 'Q1', 's': 's', 'str': 'str', 'int': 'int', 'sum': 'sum', 'ord': 'ord',
                       'char': 'char', ' ': ' '}
        self.assertEqual(15, operator[0])
        self.assertEqual(11, operand[0])
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
