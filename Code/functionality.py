import shutil
import numpy as np
from Tests import ProblemTests
import os

# Tests the functionality of python files



def TestGenerationFunctionality(source: str, probNum: int, k: int) -> int:
    """
    Tests how many generations passed the problem
    :param source: file to be tested
    :param probNum: given problem number
    :param k: total iterations
    :return: number of successful iterations
    """
    numAttempts = len(os.listdir(f"GeneratedSolutions/problem{probNum}"))
    if k != numAttempts:
        print("Incorrect amount of generated problem files")
        raise SystemError

    return sum(
        1
        for attempt in range(k)
        if CanFilePass(f"{source}{attempt}.py", probNum)
    )


def TestHumanFunctionality(source: str, probNum: int) -> int:
    """
    Tests the human solutions
    :param source:
    :param probNum:
    :return: bool
    """
    numAttempts = len(os.listdir(f"HumanSolutions/problem{probNum}"))
    return sum(
        1
        for attempt in range(numAttempts)
        if CanFilePass(f"{source}{attempt}.py", probNum)
    )


def passAtk(n,c,k):
    '''
    The probability that at least one of the top k-generated code samples for a problem passes the unit tests
    Code taken from: https://arxiv.org/pdf/2107.03374.pdf
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    :return: float
    '''
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def CanFilePass(source: str, probNum: int) -> bool:
    """
    Checks whether the give python file passes the given task
    :param source: File path
    :param probNum: Problem number
    :return: bool
    """
    # Checks if file is valid
    if not validFile(source):
        return False

    destination = "Tests/MethodTestFile.py"

    shutil.copyfile(source, destination)

    # Runs tests
    if probNum == 0:
        return CheckTests(ProblemTests.run_Q1_Tests())
    if probNum == 1:
        return CheckTests(ProblemTests.run_Q2_Tests())
    if probNum == 2:
        return CheckTests(ProblemTests.run_Q3_Tests())
    if probNum == 3:
        return CheckTests(ProblemTests.run_Q4_Tests())
    if probNum == 4:
        return CheckTests(ProblemTests.run_Q5_tests())
    return True


def CheckTests(passed):
    """
    Checks if the tests were successful or not
    :param passed: unnitest results
    :return: bool
    """
    return len(passed.failures) == 0


def validFile(source):
    """
    Checks if the file is a valid python file that can compile
    :param source: File path
    :return: bools
    """
    try:
        with open(source, 'r', encoding="utf8") as file:
            fSource = file.read()
        compile(fSource, fSource, 'exec')
        return True
    except Exception as e:
        print(f"Not valid file, Error: {e}")
        return False
