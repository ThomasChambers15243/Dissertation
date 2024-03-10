import unittest
from config import PATHS
from Code import mccabe

# File Test Name
TEST_NAME = "Complexity"


class TestScores(unittest.TestCase):
    """
    Tests against example python files
    """
    def test_zero_value(self):
        self.assertEqual(0, mccabe.get_total_value(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py"))
        self.assertEqual(0, mccabe.get_total_value(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py"))

    def test_scripts(self):
        self.assertEqual(0, mccabe.get_total_value(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py"))
        self.assertEqual(1, mccabe.get_total_value(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript2.py"))
        self.assertEqual(9, mccabe.get_total_value(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript3.py"))


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestScores)
    return unittest.TextTestRunner().run(suite)
