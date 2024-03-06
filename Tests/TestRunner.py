import LexerTests
import HalsteadTests
from config import PATHS
from loguru import logger

# Innit logger paths
logger.add(f"{PATHS['LOG_TESTING']}")

def RunLexerTests():
    """
    Runs all lexer tests
    :return:
    """
    results = LexerTests.runTests()
    # Logs results
    if results.failures:
        for result in results.failures:
            with logger.contextualize():
                logger.info(f"{result[0]} Failed")
    else:
        logger.success("Lexer Tests Passed")


def RunHalsteadTests():
    """
    Runs all halstead tests
    :return:
    """
    results = HalsteadTests.RunTests()
    # Logs results
    if results.failures:
        for result in results.failures:
            with logger.contextualize():
                logger.info(f"{result[0]} Failed")
    else:
        logger.success("Halstead Tests Passed")



def RunAllTests():
    """
    Runs all units tests
    :return:
    """
    RunLexerTests()
    RunHalsteadTests()

RunAllTests()