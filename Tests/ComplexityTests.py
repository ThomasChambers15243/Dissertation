import unittest
from config import PATHS
from Code import mccabe

TEST_NAME = "Complexity"

class TestScores(unittest.TestCase):
    def test_zero_value(self):
        self.assertEqual(0, mccabe.GetTotalValue(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py"))
        self.assertEqual(0, mccabe.GetTotalValue(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py"))
    def test_scripts(self):
        self.assertEqual(0, mccabe.GetTotalValue(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py"))
        self.assertEqual(1, mccabe.GetTotalValue(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript2.py"))
        self.assertEqual(9, mccabe.GetTotalValue(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript3.py"))

def RunTests():
    Suite = unittest.TestLoader().loadTestsFromTestCase(TestScores)
    return unittest.TextTestRunner().run(Suite)
