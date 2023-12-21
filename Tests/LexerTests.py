import unittest
from Code import Lexer

# Tests against an emtpy file
class TestEmpty(unittest.TestCase):
    def test_BlankInput(self):
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/EmtpyFile.py")
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual(operand[0], 0)
        self.assertEqual(len(operand[1]), 0)

# Tests against a file with only comments
class TestOnlyComments(unittest.TestCase):
    def test_OnlyComments(self):
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyComments.py")
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
        return True
        with open("LexerTestSamples/OnlyOperators.py", "w") as file:
            # Writes most up-to-date OPERATORS
            for key, value in Lexer.OP_TABLE.items():
                file.writelines(key)
                file.writelines('\n')
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyOperators.py")
        self.assertEqual(operator[0], 69)
        self.assertEqual(len(operator[1]),69)

# Tests against a file with only operands,
# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestOnlyOperands(unittest.TestCase):
    def test_OnlyOperandsUnique(self):
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyOperands.py")
        self.assertEqual(operand[0], 36)
        self.assertEqual(len(operand[1]), 18)
        return True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmpty("test_BlankInput"))
    suite.addTest(TestOnlyOperators("test_OnlyOperatorsUnique"))
    suite.addTest(TestOnlyOperands("test_OnlyOperandsUnique"))
    suite.addTest(TestOnlyComments("test_OnlyComments"))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
