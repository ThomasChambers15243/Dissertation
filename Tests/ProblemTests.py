import unittest
import random
import importlib
from Tests import MethodTestFile

# How to test each method in each test file?
# Write the contents of each tests file to MethodTestFile.py as the method to use.
# Test it, if it passes, then benchmark it.
# Clear the file and move onto the next test file.

class TestP1(unittest.TestCase):
    def test_temperature_conversion(self):
        importlib.reload(MethodTestFile)
        self.assertEqual(MethodTestFile.P1(0), [273.15, 32.00])
        self.assertEqual(MethodTestFile.P1(100), [373.15, 212.00])
        self.assertEqual(MethodTestFile.P1(-273.15), [0.00, -459.67])
        self.assertEqual(MethodTestFile.P1(37), [310.15, 98.60])

class TestP2(unittest.TestCase):
    def test_valid_brackets(self):
        importlib.reload(MethodTestFile)
        valid = ["()", "[]", "{}", "()[]{}", "{[()]}"]
        for i in valid:
            self.assertTrue(MethodTestFile.P2(i))
    def test_invalid_brackets(self):
        importlib.reload(MethodTestFile)
        invalid = ["((","))","({","})","][","}{","({[","]})","({[)}]"]
        for i in invalid:
            self.assertFalse(MethodTestFile.P2(i))



class TestP3(unittest.TestCase):
    def test_valid_longest_sequence(self):
        importlib.reload(MethodTestFile)
        valid = [("",0),("a",1),("abcdefg",1),("aaa",3),("abcdeeeefghi",4),("bbbbba",5),
                 ("ef3{'as;d12909999999",7),("01001000 01101001 00111010 00101001",3)]
        for i in valid:
            self.assertEqual(MethodTestFile.P3(i[0]), i[1])

class TestP4(unittest.TestCase):
    def test_duplicate_strings(self):
        importlib.reload(MethodTestFile)
        self.assertEqual(MethodTestFile.P4(["a"]), 1)
        self.assertEqual(MethodTestFile.P4(["a", "b", "c", "d", "e"]), 5)
        self.assertEqual(MethodTestFile.P4(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e"]), 5)
        self.assertEqual(MethodTestFile.P4(["abc", "abc", "cba", "abc", "zzz"]), 3)

class TestP5(unittest.TestCase):
    def test_sort_array(self):
        importlib.reload(MethodTestFile)
        valid = [([3,1,2],[1,2,3]),([5,4,3,2,1],[1,2,3,4,5]),
                 ([1,1,1,1,1],[1,1,1,1,1]),([1],[1]),
                 ([-1,-2,-3],[-3,-2,-1])]
        for i in valid:
            self.assertEqual(MethodTestFile.P5(i[0]), i[1])
    def test_large_array(self):
        importlib.reload(MethodTestFile)
        large_array = list(range(-2**16, 2**16))
        shuffled = random.sample(large_array, len(large_array))
        self.assertEqual(MethodTestFile.P5(shuffled), large_array)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestP1('test_temperature_conversion'))
    suite.addTest(TestP2('test_valid_brackets'))
    suite.addTest(TestP2('test_invalid_brackets'))
    #suite.addTest(TestP3('test_valid_longest_sequence'))
    suite.addTest(TestP4('test_duplicate_dtrings'))
    suite.addTest(TestP5('test_sort_array'))
    suite.addTest(TestP5('test_large_array'))
    return suite

# https://docs.python.org/2/library/unittest.html#unittest.TestResult

# Call Tests from out side of Code

def runTestP1():
    Suite_Test1 = unittest.TestLoader().loadTestsFromTestCase(TestP1)
    return unittest.TextTestRunner().run(Suite_Test1)
def runTestP2():
    Suite_Test2 = unittest.TestLoader().loadTestsFromTestCase(TestP2)
    return unittest.TextTestRunner().run(Suite_Test2)
def runTestP3():
    Suite_Test3 = unittest.TestLoader().loadTestsFromTestCase(TestP3)
    return unittest.TextTestRunner().run(Suite_Test3)
def runTestP4():
    Suite_Test4 = unittest.TestLoader().loadTestsFromTestCase(TestP4)
    return unittest.TextTestRunner().run(Suite_Test4)
def runTestP5():
    Suite_Test5 = unittest.TestLoader().loadTestsFromTestCase(TestP5)
    return unittest.TextTestRunner().run(Suite_Test5)





if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
