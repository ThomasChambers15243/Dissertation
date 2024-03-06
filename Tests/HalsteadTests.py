import unittest
from config import PATHS
from Code import Analyzer

class TestEmpty(unittest.TestCase):
    def test_empty(self):
        expectedMetrics = {
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
        realMetrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}EmtpyFile.py").Metrics
        self.assertDictEqual(expectedMetrics, realMetrics)


class TestOperandsWithComments(unittest.TestCase):
    def test_OperandsWithComments(self):
        expectedMetrics = {
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
        realMetrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}OnlyComments.py").Metrics
        self.assertDictEqual(expectedMetrics, realMetrics)


class TestExampleScript(unittest.TestCase):
    def testScript_1(self):
        expectedMetrics = {
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
        realMetrics = Analyzer.HalsteadMetrics(f"{PATHS['PYTHON_FILE_TEST_SAMPLES']}ExampleScript1.py").Metrics
        self.assertDictEqual(expectedMetrics, realMetrics)


def RunTests():
    Suite = unittest.TestLoader().loadTestsFromTestCase(TestEmpty)
    Suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOperandsWithComments))
    return unittest.TextTestRunner().run(Suite)
