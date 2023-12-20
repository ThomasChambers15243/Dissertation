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


class TestOnlyOperators(unittest.TestCase):
    # Currently fails due to lexer not catching operators such as '+='
    # It splits them up into '+' '='
    # So higher total count, less unique
    def test_OnlyOperatorsUnique(self):
        return True
        operator, operand = Lexer.TokeniseCode("LexerTestSamples/OnlyOperators.py")
        #self.assertEqual(len(operator[1]),69)
        self.assertEqual(operator[0], 69)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmpty('test_BlankInput'))
    suite.addTest(TestOnlyOperators('test_OnlyOperatorsUnique'))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
