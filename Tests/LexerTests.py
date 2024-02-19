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
    def test_script1(self):
        lexer = newLexer.Lexer()
        operator, operand = lexer.TokeniseCode("TestFiles/LexerTestSamples/ExampleScript1.py")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmpty("test_BlankInput"))
    suite.addTest(TestOnlyOperators("test_OnlyOperatorsUnique"))
    suite.addTest(TestOnlyOperands("test_OnlyOperandsUnique"))
    suite.addTest(TestOnlyComments("test_OnlyComments"))
    suite.addTest(TestExampleScripts("test_script1"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
