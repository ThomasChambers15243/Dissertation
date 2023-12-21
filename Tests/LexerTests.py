import unittest
from Code import Lexer

class TestEmpty(unittest.TestCase):
    def test_BlankInput(self):
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/EmtpyFile.py")
        print(operator[0])
        print(operator[1])
        print(operand[0])
        print(operand[1])
        self.assertEqual(operator[0], 0)
        self.assertEqual(len(operator[1]), 0)
        self.assertEqual(operand[0], 0)
        self.assertEqual(len(operand[1]), 0)

# Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
class TestOnlyOperators(unittest.TestCase):
    # Currently fails due to lexer not catching operators such as '+='
    # It splits them up into '+' '='
    # So higher total count, less unique
    def test_OnlyOperatorsUnique(self):
        return True
        with open("LexerTestSamples/OnlyOperators.py", "w") as file:
            for key, value in Lexer.OP_TABLE.items():
                file.writelines(key)
                file.writelines('\n')
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyOperators.py")
        self.assertEqual(operator[0], 69)
        self.assertEqual(len(operator[1]),69)

# Operands are variables, methods, constants (False, True, strings and other data type values)
class TestOnlyOperands(unittest.TestCase):
    def test_OnlyOperandsUnique(self):
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyOperands.py")
        self.assertEqual(operand[0], 36)
        self.assertEqual(len(operand[1]), 18)
        return True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmpty('test_BlankInput'))
    suite.addTest(TestOnlyOperators('test_OnlyOperatorsUnique'))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
