import shutil
import numpy as np
from Tests import ProblemTests
'''
Tests the functionality of python files
'''

def TestFunctionality(source, probNum, k):
    '''
    Tests how many generations passed the task
    :param source: file to be tested
    :param probNum: given problem number
    :param k: total iterations
    :return: number of successful iterations
    '''
    passed = 0
    for i in range(k):
        file = f"{source}{i}.py"
        functionality = CanFilePass(file, probNum)
        if functionality:
            passed += 1
        print('')
    return passed



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


def CanFilePass(source, probNum):
    '''
    Checks Whether the python file passes the given task
    Returns True if successful, else False
    '''
    # Checks if file is valid
    if not validFile(source):
        return False

    destination = "Tests/MethodTestFile.py"

    shutil.copyfile(source, destination)
    if probNum == 0:
        return CheckTests(ProblemTests.runTestP1())
    if probNum == 1:
        return CheckTests(ProblemTests.runTestP2())
    if probNum == 2:
        return CheckTests(ProblemTests.runTestP3())
    if probNum == 3:
        return CheckTests(ProblemTests.runTestP4())
    if probNum == 4:
        return CheckTests(ProblemTests.runTestP5())
    return True



'''
Checks if the tests passed. 
Returns False if their were errors,
else True
'''
def CheckTests(passed):
    print(passed.failures)
    if len(passed.failures) > 0:
        return False
    return True

'''
Checks if the file if a valid python file, free of syntax errors
'''
def validFile(source):
    try:
        with open(source, 'r') as file:
            fSource = file.read()
        compile(fSource, fSource, 'exec')
        return True
    except Exception as e:
        return False