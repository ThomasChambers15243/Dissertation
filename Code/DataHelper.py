import os
import csv
from tqdm import tqdm
from Code import mccabe
from Code import Analyzer
from Code import functionality

# Including functionality and passed counts in here
# are a little messy, however they need to be called before
# collecting metrics - so its more efficient to get them
# all in one method


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
            # Moved out to test metrics regardless of functionality
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
    Clears the given file of all data so it just one empty line
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
