import os
import sys
import argparse
from loguru import logger
from Code.Gather import Gather
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

    # Critical Arguments
    parser.add_argument("--dataCollection", "-dc", "-DC", choices=["gen", "h"],
                        help="The type of data collection, 'h' for human, 'gen' for generation")
    parser.add_argument("--sampleCollection", "-sc", "-SC", action="store_true")
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
        if not args.dataCollection and not args.sampleCollection:
            logger.error("Missing args, either dataCollection (-dc) or sampleCollection (-sc) must be used")
            return False
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
        logger.error(f"Error: Invalid data collection. Must be: gen || h, not {args.dataCollection}")
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
        if args.K_iterations < 1 or args.K_iterations >= 100:
            logger.error(f"Error: Invalid K. Must be 1 <= K <= 100, not {args.K_iterations}")
            return False
    # Data collection for human files
    # else:
    #     for prob_num in range(5):
    #         num_attempts = len(os.listdir(f"HumanSolutions/problem{prob_num}"))
    #         if args.K_iterations != num_attempts:
    #             logger.error("Incorrect amount of generated problem files")
    #             return False
    return True


@logger.catch
def run_study():
    """
    Runs the study depending on the passed through args
    :return:
    """
    args = parser_arguments()
    logger.success(f"Valid Args passed of: DataCollection: {args.dataCollection}, "
                   f"SampleCollection: {args.sampleCollection}, K: {args.K_iterations},  "
                   f"Temperature: {args.temperature}")

    # Update Config
    STUDY_PARAMS["K_ITERATIONS"] = args.K_iterations
    STUDY_PARAMS["TEMPERATURE"] = args.temperature

    # Creates instance with config file
    data_gather = Gather(STUDY_PARAMS)

    logger.info("data_gather initialized")

    ### Collect data in csv files ###

    # Human Collection
    if args.dataCollection == 'h':
        logger.info("Starting Human Collection")
        try:
            data_gather.get_human_data()
        except Exception as e:
            logger.error(f"Human Data collection failed. Error: {e}")
        else:
            logger.success("Human Data collection was successful")
    elif args.dataCollection == 'gen':
        try:
            logger.info("Starting Generation Data Collection")
            data_gather.get_gpt_data()
            logger.success("Finished Generation Data Collection")
        except Exception as e:
            logger.error(f"Generation Collection failed. Error: {e}")
    elif args.sampleCollection:
        try:
            logger.info(f"Starting gpt sample collection for k: {args.K_iterations} & T: {args.temperature}")
            data_gather.generate_gpt_solution(args.K_iterations)
            logger.success("GPT sample generation successful.")
        except Exception as e:
            logger.error(f"GPT sample generation failed. Error: {e}")
    else:
        logger.error("Incorrect Params")


if __name__ == '__main__':
    run_study()
