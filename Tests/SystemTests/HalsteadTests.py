import unittest
from config import PATHS, NULL_STREAM
from Code import Analyzer

# File Test Name
TEST_NAME = "Halstead"

class TestEmpty(unittest.TestCase):
    """
    Tests against an empty file
    """
    def test_empty(self):
        expected_metrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 0,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 0,
            "Vocabulary": 0,
            "Length": 0,
            "EstProgLength": 0,
            "Volume": 0,
            "Difficulty": 0,
            "Effort": 0,
            "Time": 0,
            "BugsEstimate": 0
        }
        real_metrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py").metrics
        self.assertDictEqual(expected_metrics, real_metrics)


class TestOperandsWithComments(unittest.TestCase):
    """
    Tests with for operands in mostly comment file
    """
    def test_OperandsWithComments(self):
        expected_metrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 2,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 2,
            "Vocabulary": 2,
            "Length": 2,
            "EstProgLength": 0,
            "Volume": 2,
            "Difficulty": 0,
            "Effort": 0,
            "Time": 0,
            "BugsEstimate": 0.0
        }
        real_metrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py").metrics
        self.assertDictEqual(expected_metrics, real_metrics)


class TestExampleScript(unittest.TestCase):
    """
    Tests against example python scripts
    """
    def testScript_1(self):
        expected_metrics = {
            "DistinctOperatorCount": 3,
            "DistinctOperandCount": 6,
            "TotalOperatorCount": 4,
            "TotalOperandCount": 6,
            "Vocabulary": 9,
            "Length": 9,
            "EstProgLength": 20.26,
            "Volume": 28.53,
            "Difficulty": 1.5,
            "Effort": 42.8,
            "Time": 2.38,
            "BugsEstimate": 0.01
        }
        real_metrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py").metrics
        self.assertDictEqual(expected_metrics, real_metrics)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmpty)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOperandsWithComments))
    return unittest.TextTestRunner(stream=NULL_STREAM).run(suite)
