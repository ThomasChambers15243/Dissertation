import unittest
from config import PATHS
from Code import mccabe


class TestEmpty(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


def RunTests():
    Suite = unittest.TestLoader.loadTestsFromTestCase(TestEmpty)
    #Suite.addTests(unittest.TestLoader.loadTestsFromTestCase())
    return unittest.TextTestRunner().run(Suite)

RunTests()