import unittest
import sys
import random
from TestFile import P1
from TestFile import P2
from TestFile import P3
from TestFile import P4
from TestFile import P5
from TestFile import P6

class TestP1(unittest.TestCase):
    def test_temperature_conversion(self):
        self.assertEqual(P1(0), [273.15, 32.00])
        self.assertEqual(P1(100), [373.15, 212.00])
        self.assertEqual(P1(-273.15), [0.00, -459.67])
        self.assertEqual(P1(37), [310.15, 98.60])

class TestP2(unittest.TestCase):
    def test_valid_brackets(self):
        self.assertTrue(P2("()"))
        self.assertTrue(P2("[]"))
        self.assertTrue(P2("{}"))
        self.assertTrue(P2("()[]{}"))
        self.assertTrue(P2("{[()]}"))
    def test_invalid_brackets(self):
        self.assertFalse(P2("(("))
        self.assertFalse(P2("))"))
        self.assertFalse(P2("({"))
        self.assertFalse(P2(")}"))
        self.assertFalse(P2("]["))
        self.assertFalse(P2("}{"))
        self.assertFalse(P2("({["))
        self.assertFalse(P2("]})"))
        self.assertFalse(P2("({[)}]"))

class TestP3(unittest.TestCase):
    def test_longest_sequence(self):
        self.assertEqual(P3(""), 0)
        self.assertEqual(P3("a"), 1)
        self.assertEqual(P3("abcdefg"), 1)
        self.assertEqual(P3("aaa"), 3)
        self.assertEqual(P3("abcdeeeefghi"), 4)
        self.assertEqual(P3("bbbbba"), 5)
        self.assertEqual(P3("ef3{'as;d12909999999"), 7)
        self.assertEqual(P3("01001000 01101001 00111010 00101001"), 3)

class TestP4(unittest.TestCase):
    def test_duplicate_strings(self):
        self.assertEqual(P4(["a"]), 1)
        self.assertEqual(P4(["a", "b", "c", "d", "e"]), 5)
        self.assertEqual(P4(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e"]), 5)
        self.assertEqual(P4(["abc", "abc", "cba", "abc", "zzz"]), 3)

class TestP5(unittest.TestCase):
    def test_sort_array(self):
        self.assertEqual(P5([]), [])
        self.assertEqual(P5([3, 1, 2]), [1, 2, 3])
        self.assertEqual(P5([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
        self.assertEqual(P5([1, 1, 1, 1, 1]), [1, 1, 1, 1, 1])
        self.assertEqual(P5([1]), [1])
        self.assertEqual(P5([-1, -2, -3]), [-3, -2, -1])
    def test_large_array(self):
        large_array = [i for i in range(-2**16, 2**16)]
        shuffled = random.sample(large_array, len(large_array))
        self.assertEqual(P5(shuffled), large_array)

class TestP6(unittest.TestCase):
    def test_combine_and_sort_arrays(self):
        self.assertEqual(P6([], []), [])
        self.assertEqual(P6(["a","aa","aaa","aaaa","aaaaa",], ["b","bb","bbb","bbbb", "bbbbb"]), ["a","b","aa","bb","aaa","bbb","aaaa","bbbb","aaaaa","bbbbb"])
        self.assertEqual(P6(["abc", "de"], []), ["de", "abc"])
        self.assertEqual(P6([], ["f", "ghi"]), ["f", "ghi"])
        self.assertEqual(P6(["abc", "de"], ["f", "ghi"]), ["f", "de", "abc", "ghi"])
        self.assertEqual(P6(["abc", "de"], ["f", "gh"]), ["f", "de", "gh", "abc"])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestP1('test_temperature_conversion'))
    suite.addTest(TestP2('test_valid_brackets'))
    suite.addTest(TestP2('test_invalid_brackets'))
    suite.addTest(TestP3('test_longest_sequence'))
    suite.addTest(TestP4('test_duplicate_dtrings'))
    suite.addTest(TestP5('test_sort_array'))
    suite.addTest(TestP5('test_large_array'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())