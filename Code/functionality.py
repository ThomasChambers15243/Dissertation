import shutil
import os
import sys
import io
import numpy as np
from Tests import ProblemTests
from config import PATHS
from loguru import logger

### Tests the functionality of python files ###



def test_generation_functionality(source: str, prob_num: int, k: int) -> int:
    """
    Tests how many generations passed the problem
    :param source: file to be tested
    :param prob_num: given problem number
    :param k: total iterations
    :return: number of successful iterations
    """
    num_attempts = len(os.listdir(f"GeneratedSolutions/problem{prob_num}"))
    if k != num_attempts:
        print("Incorrect amount of generated problem files")
        raise SystemError

    # Tests functionality
    return sum(
        1
        for attempt in range(num_attempts)
        if can_file_pass(f"{source}{attempt}.py", prob_num)
    )


def pass_atk(n: float, c: float, k: float) -> float:
    """
    The probability that at least one of the top k-generated code samples for a problem passes the unit tests
    Code taken from: https://arxiv.org/pdf/2107.03374.pdf
    Good explenation - https://deepgram.com/learn/humaneval-llm-benchmark#the-passk-metric
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    :return: Pass@k value as float
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def can_file_pass(source: str, prob_num: int) -> bool:
    """
    Checks whether the give python file passes the given task
    :param source: File path
    :param prob_num: Problem number
    :return: Bool value, True if pass, else False
    """
    # Checks if file is valid
    if not valid_file(source):
        return False

    # Copies file to be tested into test file so that unit tests can find it
    shutil.copyfile(source, PATHS["METHOD_TEST_FILE"])

    # Suppress console output from files ran
    suppress_text = io.StringIO()
    sys.stdout = suppress_text
    results = False
    # Runs tests
    if prob_num == 0:
        results = ProblemTests.run_q1_tests()
    elif prob_num == 1:
        results = ProblemTests.run_q2_tests()
    elif prob_num == 2:
        results = ProblemTests.run_q3_tests()
    elif prob_num == 3:
        results = ProblemTests.run_q4_tests()
    elif prob_num == 4:
        results = ProblemTests.run_q5_tests()
    sys.stdout = sys.__stdout__
    return check_tests(results)


def check_tests(passed) -> bool:
    """
    Checks if the unit tests were successful or not
    :param passed: unnitest results
    :return: True if passed, else false
    """
    return len(passed.failures) == 0 and len(passed.errors) == 0


def valid_file(source: str):
    """
    Checks if the file is a valid python file that can compile
    :param source: File path
    :return: Bool, true if valid python file, else false
    """
    try:
        with open(source, 'r', encoding="utf8") as file:
            f_source = file.read()
        compile(f_source, f_source, 'exec')
        return True
    except Exception:
        return False
