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




def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmpty('test_BlankInput'))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
