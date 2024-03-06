# Resets the file
open("Tests/MethodTestFile.py", 'w').close()
import argparse
import os
from config import STUDY_PARAMS
from Code.Gather import Gather


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
        print("Missing args dataCollection (-dc)")
        return False
    if not args.temperature:
        print("Missing args temperature(-t)")
        return False
    if not args.K_iterations:
        print("Missing args k_iterations (-k)")
        return False
    return True


def fitRules(args) -> bool:
    """
    :param args: CLI arguments
    :return: bool
    """
    # Checks Arguments are valid
    if args.dataCollection not in ["gen", "h"]:
        print(f"\nError: Invalid data collection. Must be: gen || h, not {args.dataCollection}\n")
        return False
    # Data collection for generations
    if args.dataCollection == "gen":
        if not args.temperature:
            print("\nError: Must input temperature: -t {int}")
            return False
        if args.temperature <= 0 or args.temperature > 1:
            print(f"\nError: Invalid temperature. Must be 0 < T <= 1, not {args.temperature}\n")
            return False
        if not args.K_iterations:
            print("Must input iterations, -k {int}")
            return False
        if args.K_iterations < 1 or args.K_iterations >= 100:
            print(f"\nError: Invalid K. Must be 1 <= K <= 100, not {args.K_iterations}\n")
            return False
    # Data collection for human files
    else:
        for probNum in range(5):
            numAttempts = len(os.listdir(f"HumanSolutions/problem{probNum}"))
            if args.K_iterations != numAttempts:
                print("Incorrect amount of generated problem files")
                return False
    return True

if __name__ == '__main__':
    # Get args
    args = parserArguemts()

    # Update Config
    STUDY_PARAMS["K_ITERATIONS"] = args.K_iterations
    STUDY_PARAMS["TEMPERATURE"] = args.temperature

    # Creates instance with config file
    DataGather = Gather(STUDY_PARAMS)

    # Collect data in csv files
    if args.dataCollection == 'h':
        print("running human collection")
        DataGather.GetHumanData()
    elif args.dataCollection == 'gen' and STUDY_PARAMS["K_ITERATIONS"] <= 100:
        print("Running generation collection")
        DataGather.GetGPTData(args.temperature)
    else:
        print("Incorrect params")
