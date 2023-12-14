import unittest
import random
from TestFile import P1
from TestFile import P2
from TestFile import P3
from TestFile import P4
from TestFile import P5
from TestFile import P6

# How to test each method in each test file?
# Write the contents of each tests file to TestFile.py as the method to use.
# Test it, if it passes, then benchmark it.
# Clear the file and move onto the next test file.

class TestP1(unittest.TestCase):
    def test_temperature_conversion(self):
        self.assertEqual(P1(0), [273.15, 32.00])
        self.assertEqual(P1(100), [373.15, 212.00])
        self.assertEqual(P1(-273.15), [0.00, -459.67])
        self.assertEqual(P1(37), [310.15, 98.60])

class TestP2(unittest.TestCase):
    def test_valid_brackets(self):
        valid = ["()", "[]", "{}", "()[]{}", "{[()]}"]
        for i in valid:
            self.assertTrue(P2(i))
    def test_invalid_brackets(self):
        invalid = ["((","))","({","})","][","}{","({[","]})","({[)}]"]
        for i in invalid:
            self.assertFalse(P2(i))

class TestP3(unittest.TestCase):
    def test_valid_longest_sequence(self):
        valid = [("",0),("a",1),("abcdefg",1),("aaa",3),("abcdeeeefghi",4),("bbbbba",5),
                 ("ef3{'as;d12909999999",7),("01001000 01101001 00111010 00101001",3)]
        for i in valid:
                self.assertEqual(P3(i[0]), i[1])

class TestP4(unittest.TestCase):
    def test_duplicate_strings(self):
        self.assertEqual(P4(["a"]), 1)
        self.assertEqual(P4(["a", "b", "c", "d", "e"]), 5)
        self.assertEqual(P4(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e"]), 5)
        self.assertEqual(P4(["abc", "abc", "cba", "abc", "zzz"]), 3)

class TestP5(unittest.TestCase):
    def test_sort_array(self):
        valid = [([3,1,2],[1,2,3]),([5,4,3,2,1],[1,2,3,4,5]),
                 ([1,1,1,1,1],[1,1,1,1,1]),([1],[1]),
                 ([-1,-2,-3],[-3,-2,-1])]
        for i in valid:
            self.assertEqual(P5(i[0]), i[1])
    def test_large_array(self):
        large_array = list(range(-2**16, 2**16))
        shuffled = random.sample(large_array, len(large_array))
        self.assertEqual(P5(shuffled), large_array)

class TestP6(unittest.TestCase):
    def test_combine_and_sort_arrays(self):
        valid = [([],[],[]),(["a","aa","aaa","aaaa","aaaaa",],["b","bb","bbb","bbbb", "bbbbb"],
                            ["a","b","aa","bb","aaa","bbb","aaaa","bbbb","aaaaa","bbbbb"]),
                            (["abc", "de"],[],["de", "abc"]),([],["f", "ghi"],["f", "ghi"]),
                            (["abc", "de"], ["f", "ghi"],["f", "de", "abc", "ghi"]),
                            (["abc", "de"], ["f", "gh"],["f", "de", "gh", "abc"])]
        for i in valid:
            self.assertEqual(P6(i[0],i[1]), i[2])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestP1('test_temperature_conversion'))
    suite.addTest(TestP2('test_valid_brackets'))
    suite.addTest(TestP2('test_invalid_brackets'))
    suite.addTest(TestP3('test_valid_longest_sequence'))
    suite.addTest(TestP4('test_duplicate_dtrings'))
    suite.addTest(TestP5('test_sort_array'))
    suite.addTest(TestP5('test_large_array'))
    return suite

# https://docs.python.org/2/library/unittest.html#unittest.TestResult

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    a = runner.run(suite())
    print(a)
