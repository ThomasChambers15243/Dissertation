import argparse
import os
import sys
import traceback

from loguru import logger
from config import STUDY_PARAMS, PATHS
from Code.Gather import Gather

# Resets the file
open("Tests/MethodTestFile.py", 'w').close()

# Innit Logger
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(f"{PATHS['LOG_MAIN']}")


def parserArguemts():
    """
    Gets arguments passed
    :return: namespace of arguments
    """

    # Gets passed through arguments
    parser = argparse.ArgumentParser()

    # Critical Arguments
    parser.add_argument("--dataCollection", "-dc", "-DC", choices=["gen", "h"],
                        help="The type of data collection, 'h' for human, 'gen' for generation")
    parser.add_argument("--temperature", "-t", "-T", type=float,
                        help="The temperature to use for the GPT-3 API")
    parser.add_argument("--K_iterations", "-k", "-K", type=int,
                        help="The amount of times to run the study. K in pass@k")

    # Optional Arguments
    parser.add_argument("--sampleCSVPath", "-sCSVp", default="Code/data/SampleResults.csv",
                        help="The path to store the generated CSV")
    parser.add_argument("--humanCSVPath", "-hCSVp", default="Code/data/HumanResults.csv",
                        help="The path to store the human results in")
    parser.add_argument("--genSolutionsPath", "-gSP", default="GeneratedSolutions/",
                        help="The path to store the generated solutions in")
    parser.add_argument("--humanSolutionsPath", "-hSP", default="HumanSolutions/",
                        help="The path to store the human solutions in")
    parser.add_argument("--problemsPath", "-pP", default="Code/data/ProblemQuestions.json",
                        help="The path to the problems json file")
    parser.add_argument("--problemAmount", "-pA", default=5, type=int,
                        help="The amount of problems to generate")

    args = parser.parse_args()

    # Checks Arguments exist
    if areValidArgs(args):
        return args
    raise SystemExit


def areValidArgs(args) -> bool:
    """
    Checks if the arguments are valid
    :param args: cli arguments
    :return: bool
    """
    if not argsExists(args):
        return False
    return fitRules(args)


def argsExists(args) -> bool:
    """
    Checks if the arguments exit
    :param args: CLI arguments
    :return: bool
    """
    if not args.dataCollection:
        logger.error("Missing args dataCollection (-dc)")
        return False
    if not args.K_iterations:
        logger.error("Missing args k_iterations (-k)")
        return False
    return True


def fitRules(args) -> bool:
    """
    :param args: CLI arguments
    :return: bool
    """
    # Checks Arguments are valid
    if args.dataCollection not in ["gen", "h"]:
        logger.error(f"Error: Invalid data collection. Must be: gen || h, not {args.dataCollection}")
        return False
    # Data collection for generations
    if args.dataCollection == "gen":
        if not args.temperature:
            logger.error("Error: Must input temperature: -t {int}")
            return False
        if args.temperature <= 0 or args.temperature > 1:
            logger.error(f"Error: Invalid temperature. Must be 0 < T <= 1, not {args.temperature}")
            return False
        if not args.K_iterations:
            logger.error("Must input iterations, -k {int}")
            return False
        if args.K_iterations < 1 or args.K_iterations >= 100:
            logger.error(f"Error: Invalid K. Must be 1 <= K <= 100, not {args.K_iterations}")
            return False
    # Data collection for human files
    else:
        for probNum in range(5):
            numAttempts = len(os.listdir(f"HumanSolutions/problem{probNum}"))
            if args.K_iterations != numAttempts:
                logger.error("Incorrect amount of generated problem files")
                return False
    return True


@logger.catch
def RunStudy():
    # Get args
    args = parserArguemts()
    logger.success(f"Valid Args passed of: DataCollection: {args.dataCollection},  K: {args.K_iterations},  "
                   f"Temperature: {args.temperature}")

    # Update Config
    STUDY_PARAMS["K_ITERATIONS"] = args.K_iterations
    STUDY_PARAMS["TEMPERATURE"] = args.temperature

    # Creates instance with config file
    DataGather = Gather(STUDY_PARAMS)

    logger.info("DataGather initialized")

    ### Collect data in csv files ###

    # Human Collection
    if args.dataCollection == 'h':
        logger.info("Starting Human Collection")
        try:
            DataGather.GetHumanData()
        except Exception:
            logger.error("Human Data collection failed")
        else:
            logger.success("Human Data collection was successful")
    elif args.dataCollection == 'gen' and STUDY_PARAMS["K_ITERATIONS"] <= 100:
        logger.info("Starting Generation Collection")
        try:
            DataGather.GetGPTData(args.temperature)
        except Exception:
            logger.error("Generation Collection failed")
        else:
            logger.success("Finished Generation Collection")
    else:
        logger.error("Incorrect Params")


if __name__ == '__main__':
    RunStudy()
