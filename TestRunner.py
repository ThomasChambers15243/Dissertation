import Tests.LexerTests as LexerTests
import Tests.HalsteadTests as HalsteadTests
import Tests.ComplexityTests as ComplexityTests
from config import PATHS
from loguru import logger

# Innit logger paths
logger.add(f"{PATHS['LOG_TESTING']}")


def RunTest(methodObj):
    """
    Runs and logs the results of the test obj passed through
    :param methodObj: testfile obj
    :return: bool, true if passed, false if failed
    """
    results = methodObj.RunTests()
    # Logs results
    if results.failures:
        for result in results.failures:
            with logger.contextualize():
                logger.info(f"{result[0]} Failed")
        return False
    else:
        logger.success(f"{methodObj.TEST_NAME} Tests Passed")
        return True


def RunAllTests():
    """
    Runs all units tests
    :return:
    """
    RunTest(LexerTests)
    RunTest(HalsteadTests)
    RunTest(ComplexityTests)

# RunAllTests()
