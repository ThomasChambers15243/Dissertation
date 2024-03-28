import os
import csv
from distutils.dir_util import copy_tree
import shutil
import csv
from config import PATHS
from tqdm import tqdm
from loguru import logger
from Code import mccabe
from Code import Analyzer
from Code import functionality

# Innit Logger
logger.add(f"{PATHS['LOG_MAIN']}", level="INFO")

"""
Including functionality and passed counts in here
are a little messy, however they need to be called before
collecting metrics - so its more efficient to get them
all in one method
 """


def get_metrics(prob_num: int, num_of_solutions: int, source: str) -> tuple[list[dict], int, int]:
    """
    Gets the metrics of each solution in a dict
    and returns a tuple - list of all dics containing metrics,
    non-valid, passed
    :param prob_num: The problem number for metric collection
    :param num_of_solutions: number of solutions in dir
    :param source: The file path containing the solution
    :return: All metrics in [{metrics}], non-valid, passed
    """
    all_metrics = []
    passed = 0
    invalid = 0
    for attempt in tqdm(range(num_of_solutions),
                        desc=f"\033[33mGetting Metrics",
                        ncols=80,
                        leave=False):
        # Dictionary to hold the sum total of metrics
        metrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 0,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 0,
            "Vocabulary": 0,
            "Length": 0,
            "EstProgLength": 0,
            "Volume": 0,
            "Difficulty": 0,
            "Effort": 0,
            "Time": 0,
            "BugsEstimate": 0,
            "MccabeComplexity": 0}
        k_file = f"{source}{attempt}.py"

        # Only calculate metrics if file is valid and passes problem
        if functionality.valid_file(k_file):
            if functionality.can_file_pass(k_file, prob_num):
                passed += 1
                # Add Halstead and mccabe metric scores to dict
                # Move out to test metrics regardless of functionality
                for key, value in Analyzer.HalsteadMetrics(k_file).metrics.items():
                    metrics[key] = value
                metrics["MccabeComplexity"] = mccabe.get_total_value(k_file)
        else:
            invalid += 1
        all_metrics.append(metrics)

    return all_metrics, invalid, passed


def innit_csv(csv_path: str, headers: list) -> None:
    """
    Sets up headers for Sample Score CSV Data
    :param csv_path: Path for the csv path to be written too
    :param headers: List of headers to load into the top of the file
    :return: None
    """
    # Create CSV File with appropriate headers
    with open(f"{csv_path}", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def calculate_sample_score(metrics: dict) -> float:
    """
    Calculates one value from the entire metrics dictionary
    Needs to be updated with scoring weights
    :param metrics: All Halstead
    :return: Total score of all metrics
    """
    sample_sum = 0
    for key, value in metrics.items():
        # Increases impact of Mccabe
        if key == "MccabeComplexity":
            sample_sum += (value * 100)
        elif key in ["EstProgLength", "Effort"]:
            sample_sum += (value / 10)
        else:
            sample_sum += value
    return sample_sum


def clear_file(file_path) -> None:
    """
    Clears the given file of all Data so it just one empty line
    :return: None
    """
    open(file_path, 'w').close()


def number_of_invalid_solutions(file_path: str, k_iterations: int):
    """
    Gets how many valid python files are in the file path folder
    :param file_path: Path to solution folder
    :param k_iterations: Number of attempts
    :return: Number of valid files
    """
    not_valid = 0
    for attempt in range(k_iterations):
        k_file = f"{file_path}{attempt}.py"
        if not functionality.valid_file(k_file):
            not_valid += 1
    return not_valid


def number_of_passed_solutions(file_path: str, k_iterations: int, prob_num: int):
    """
    Gets how many solutions passed the unit tests
    :param file_path: Path to solution folder
    :param k_iterations: Number of attempts
    :param prob_num: Problem number currently being tested
    :return: Number of solutions that passed
    """
    passed = 0
    for attempt in range(k_iterations):
        k_file = f"{file_path}{attempt}.py"
        if functionality.can_file_pass(k_file, prob_num):
            passed += 1
    return passed


""" Files to handle and clean Data AFTER collection """


def load_human_files() -> bool:
    """
    Automates the loading of submissions into the directory.
    Loads all files from config PATHS dissertation_question_storage
    into PATHS human_solutions_dir_path
    :return Bool if method was successful
    """

    # Paths for questions
    dissertation_questions = PATHS["DISSERTATION_QUESTION_STORAGE"]
    dissertation_destination = PATHS["HUMAN_SOLUTIONS_DIR_PATH"]

    # Number of attempts
    solution_attempt_count = len(os.listdir(dissertation_questions))
    # Count number of files
    file_count = 0

    # For each human submission
    for submissionNum, submission in enumerate(os.listdir(dissertation_questions)):
        submissionDir = f"{dissertation_questions}/{submission}"
        # Goes through each question in each human's submission
        for questionFile in os.listdir(submissionDir):
            probNum = str(int(questionFile[9]) - 1)
            # Sets up file paths
            solutionFile = f"{dissertation_questions}/{submission}/{questionFile}"
            destinationDir = f"{dissertation_destination}problem{probNum}"
            destinationFile = f"{destinationDir}/human--n{submissionNum}.py"
            # Create problem dir if it doesn't exist
            if not os.path.exists(destinationDir):
                os.makedirs(destinationDir)
            # Copies over file
            try:
                shutil.copyfile(solutionFile, destinationFile)
                file_count += 1
            except Exception as e:
                logger.error(f"Could not copy over file. Error: {e}")
                return False

    # Log Solutions
    logger.success(f"Loaded human solution files. \n"
                   f"Total Attempts: {solution_attempt_count}.\n"
                   f"Total Files: {file_count}.")
    return True


def clean_failed_solutions(back_up=True) -> bool:
    """
    Removes all zero's (failed solutions) from human and
    generated .csv files using config PATHS.
    Backs up data by defualt and re-writes if cleaning
    fails
    :param back_up bool Backs up data before cleaning and re-writes data if
    method fails. True by defualt
    :return: bool if successful or not
    """
    # Backs up data
    if back_up:
        backup_data()

    # Cleans Data
    try:
        delete_lines("hum")
        delete_lines("gen")
    except Exception as e:
        logger.error(f"Cleaning Failed. Ensure directory's and their contents are valid. Error: {e}")
        if back_up:
            load_backup_data()
        return False

    # Deletes backed-up data
    if back_up:
        delete_backup_data()

    return True


def backup_data():
    humanPath = PATHS["HUMAN_RESULTS_CSV_DIR_PATH"]
    genPath = PATHS["SAMPLE_RESULTS_CSV_DIR_PATH"]
    copy_tree(humanPath, f"{PATHS['HUMAN_DATA_BACKUP']}")
    copy_tree(genPath, f"{PATHS['GEN_DATA_BACKUP']}")


def load_backup_data():
    raise NotImplementedError


def delete_backup_data():
    raise NotImplementedError


def delete_lines(target: str):
    """
    Deletes the lines from human and gen csv's that have
    zero'd values
    :param target: string, The directory you want to find zeros in
    :return: True if successful
    """
    # Set paths
    humanPath = PATHS["HUMAN_RESULTS_CSV_DIR_PATH"]
    genPath = PATHS["SAMPLE_RESULTS_CSV_DIR_PATH"]

    # Check length are equal
    if len(os.listdir(humanPath)) != len(os.listdir(genPath)):
        logger.error("Unequal amount of of solutions in dirs")
        return False

    # Clean solutions
    for csv_file in os.listdir(humanPath):
        # Sets paths
        human_file_path = f"{humanPath}{csv_file}"
        gen_file_path = f"{genPath}{csv_file}"
        # Get row lines to keep
        if target != 'hum':
            lines_to_keep = get_non_zeroed_lines(gen_file_path)
        else:
            lines_to_keep = get_non_zeroed_lines(human_file_path)
        # Get rows to keep
        human_rows_to_keep = get_rows_to_keep(human_file_path, lines_to_keep)
        gen_rows_to_keep = get_rows_to_keep(gen_file_path, lines_to_keep)
        # Write lines to
        write_lines(human_file_path, human_rows_to_keep,
                    gen_file_path, gen_rows_to_keep)
    return True


def write_lines(file1: str, file_one_rows: list[str],
                file2: str, file_two_rows: list[str]) -> None:
    with open(file1, "w", newline="") as one, open(file2, "w", newline="") as two:
        # Sets up writers
        writer_one = csv.writer(one)
        writer_two = csv.writer(two)
        # Write rows
        writer_one.writerows(file_one_rows)
        writer_two.writerows(file_two_rows)


def get_rows_to_keep(filePath: str, row_nums: list[int]) -> list:
    """
    Gets a list of rows to keep in the csv
    :param filePath: String file path
    :param row_nums: List of rows to keep
    :return: List of rows to keep
    """
    with open(filePath, "r") as file:
        csv_reader = csv.reader(file, delimiter=',')
        return [row for rowNum, row in enumerate(csv_reader)
                if rowNum in row_nums]


def get_non_zeroed_lines(filePath: str) -> list[int]:
    """
    Gets lines that equal to zero in the given file
    :param filePath: String file path
    :return: List one line numbers equal to zero
    """
    with open(filePath, "r") as file:
        csv_reader = csv.reader(file, delimiter=',')
        return [rowNum for rowNum, row in enumerate(csv_reader)
                if row[-1] != '0.0']
