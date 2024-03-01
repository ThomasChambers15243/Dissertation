open("Tests/MethodTestFile.py", 'w').close()
import argparse
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
    parser.add_argument("--problemsPath", "-pP", default="Code/data/pilotProblems.json",
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
    return argsExists(args) and fitRules(args)


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
    # TODO IS not raising a system exit/system False intentional or did i forget?
    if not args.K_iterations:
        print("Missing args k_iterations (-k)")
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
    if args.temperature <= 0 or args.temperature > 1:
        print(f"\nError: Invalid temperature. Must be 0 < T <= 1, not {args.temperature}\n")
        return False
    if args.K_iterations != 1 and args.dataCollection == "h":
        print(f"\nError: Invalid iterations for dataCollection. If dc = gen, k must equal 1, not {args.K_iterations}\n")
        return False
    if not args.K_iterations and args.dataCollection == "gen":
        print("Must input iterations, -k {num}")
        return False
    if args.K_iterations < 1 or args.K_iterations >= 100:
        print(f"\nError: Invalid K. Must be 1 <= K <= 100, not {args.K_iterations}\n")
        return False
    return True

if __name__ == '__main__':
    args = parserArguemts()

    # Set up instance for Study
    DataGather = Gather(STUDY_PARAMS)

    temperature = "0.6"

    # 'h' for human data
    # 'gen' for generations
    dataCollect = 'gen'

    # Collect data in csv files
    if args.dataCollection == 'h' and STUDY_PARAMS["K_ITERATIONS"] == 1:
        DataGather.GetHumanData()
        print("running human collection")
    elif args.dataCollection == 'gen' and STUDY_PARAMS["K_ITERATIONS"] <= 100:
        DataGather.GetGPTData(temperature)
        print("Running generation collection")
    else:
        print("Incorrect params")
