import Tests.LexerTests as LexerTests
import Tests.HalsteadTests as HalsteadTests
import Tests.ComplexityTests as ComplexityTests
from config import PATHS
from loguru import logger

# Innit logger paths
logger.add(f"{PATHS['LOG_TESTING']}")


def run_test(method_obj):
    """
    Runs and logs the results of the test obj passed through
    :param method_obj: testfile obj
    :return: bool, true if passed, false if failed
    """
    results = method_obj.run_tests()
    # Logs results
    if results.failures:
        for result in results.failures:
            with logger.contextualize():
                logger.info(f"{result[0]} Failed")
        return False
    else:
        logger.success(f"{method_obj.TEST_NAME} Tests Passed")
        return True


def run_all_tests():
    """
    Runs all units tests
    :return:
    """
    run_test(LexerTests)
    run_test(HalsteadTests)
    run_test(ComplexityTests)

# run_all_tests()
