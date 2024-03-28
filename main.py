import sys
import argparse
from loguru import logger
from Code.Gather import Gather
from Code.DataHelper import load_human_files, clean_failed_solutions
from config import STUDY_PARAMS, PATHS

# Resets the file
open("Tests/MethodTestFile.py", 'w').close()


# Filter method for logs by level
def level_filter(level):
    def is_level(record):
        return record["level"].name == level

    return is_level


# Innit Logger
# Console log/ Main log/ Results Log
logger.remove()
logger.level("Results", no=15, color="<blue>")
logger.add(sys.stderr, level="INFO")
logger.add(f"{PATHS['LOG_MAIN']}", level="INFO")
logger.add(sink=PATHS['LOG_RESULTS'], filter=level_filter("Results"))


def parser_arguments():
    """
    Gets arguments passed
    :return: namespace of arguments
    """

    # Gets passed through arguments
    parser = argparse.ArgumentParser()

    # Arguments
    # Only one of these can be used. Group has priority over other args
    wrangle = parser.add_mutually_exclusive_group()
    wrangle.add_argument("--loadHumanQuestions", "-lh", action="store_true",
                         help="Loads in human written questions using PATHS file destination"
                              "in config")

    wrangle.add_argument("--cleanFailedSolutions", "-c", "-clean", action="store_true",
                         help="Removes all values that failed from data + their matched values in"
                              "human/gen csv data. True by default.")

    parser.add_argument("--dataCollection", "-dc", "-DC", choices=["gen", "h"],
                        help="The type of Data collection, 'h' for human, 'gen' for generation")

    parser.add_argument("--sampleCollection", "-sc", "-SC", action="store_true",
                        help="Flag to collect code generation solutions. Needs -t & -k")

    parser.add_argument("--temperature", "-t", "-T", type=float,
                        help="The temperature to use for the GPT-3 API")

    parser.add_argument("--K_iterations", "-k", "-K", type=int,
                        help="The amount of times to run the study. K in pass@k")

    args = parser.parse_args()

    # Checks Arguments exist
    if are_valid_args(args):
        return args
    raise SystemExit


def are_valid_args(args) -> bool:
    """
    Checks if the arguments are valid
    :param args: cli arguments
    :return: bool
    """
    return fit_rules(args) if args_exists(args) else False


def args_exists(args) -> bool:
    """
    Checks if the arguments exit
    :param args: CLI arguments
    :return: bool
    """
    try:
        # if not args.dataCollection and not args.sampleCollection and not args.loadHumanQuestions and not args.:
        #     logger.error("Missing args, either dataCollection (-dc), sampleCollection (-sc) or"
        #                  " loadHumanQuestions (-lh) must be used")
        #     return False
        if (args.sampleCollection and not args.dataCollection) and (not args.K_iterations or not args.temperature):
            logger.error("Missing args k_iterations (-k) or temperature (-t)")
            return False
    except Exception as e:
        logger.error(f"Argument Failure. Error: {e}")
        return False

    # If all required args exist
    return True


def fit_rules(args) -> bool:
    """
    :param args: CLI arguments
    :return: bool
    """
    # Checks Arguments are valid
    if args.dataCollection and args.dataCollection not in ["gen", "h"]:
        logger.error(f"Error: Invalid Data collection. Must be: gen || h, not {args.dataCollection}")
        return False
    # Data collection for generations
    if args.sampleCollection:
        if not args.temperature:
            logger.error("Error: Must input temperature: -t {int}")
            return False
        if args.temperature <= 0 or args.temperature > 1:
            logger.error(f"Error: Invalid temperature. Must be 0 < T <= 1, not {args.temperature}")
            return False
        if not args.K_iterations:
            logger.error("Must input iterations, -k {int}")
            return False
        if args.K_iterations < 1 or args.K_iterations > 100:
            logger.error(f"Error: Invalid K. Must be 1 <= K <= 100, not {args.K_iterations}")
            return False
    return True


def sample_collection(args) -> None:
    """
    Generated code samples based on args commands
    :param args: Namespace of command-line args
    :return: None
    """

    # Update Config
    STUDY_PARAMS["K_ITERATIONS"] = args.K_iterations
    STUDY_PARAMS["TEMPERATURE"] = args.temperature

    try:
        logger.info(f"Starting gpt sample collection for k: {args.K_iterations} & T: {args.temperature}")
        # data_gather.generate_gpt_solution(args.K_iterations)
        logger.success("GPT sample generation successful.")
    except Exception as e:
        logger.error(f"GPT sample generation failed. Error: {e}")


def data_collection(args) -> None:
    """
    Collects either human or generated Data from
    code samples
    :param args: Namespace of command-line args
    :return: None
    """
    # Innit Study Class Object
    data_gather = Gather(STUDY_PARAMS)

    # Human Collection
    if args.dataCollection == 'h':
        try:
            logger.info("Starting Human Collection")
            data_gather.get_human_data()
        except Exception as e:
            logger.error(f"Human Data collection failed. Error: {e}")
        else:
            logger.success("Human Data collection was successful")
    # Generation Collection
    elif args.dataCollection == 'gen':
        try:
            logger.info("Starting Generation Data Collection")
            data_gather.get_gpt_data()
            logger.success("Finished Generation Data Collection")
        except Exception as e:
            logger.error(f"Generation Collection failed. Error: {e}")
    else:
        logger.error("Incorrect Params")


def direct_program() -> None:
    """
    Gets arguments and directs the course
    of the program, whether to interact with the study
    or to load up the study
    :return: None
    """
    args = parser_arguments()

    # Decides what the program should run
    if args.loadHumanQuestions:
        logger.success("Valid args passed for loading human questions")
        try:
            load_human_files()
        except Exception as e:
            logger.error(f"Could not load human files. Error: {e}")
    elif args.cleanFailedSolutions:
        logger.success("Valid args passed for cleaning failed solutions from dataset")
        try:
            clean_failed_solutions()
        except Exception as e:
            logger.error(f"Could not clean data. Error: {e}")
    elif args.sampleCollection:
        logger.success("Valid args pass for sample collection")
        sample_collection(args)
    elif args.dataCollection:
        logger.success("Valid args pass for Data collection")
        data_collection(args)


if __name__ == '__main__':
    direct_program()
