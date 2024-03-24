import os
import csv
from Code import mccabe
from Code import Analyzer
from Code import functionality


def get_metrics(prob_num: int, source: str) -> list[dict]:
    """
    Gets the metrics of each solution in a dict
    and returns a list of all dics
    :return: All metrics in [{metrics}]
    """
    all_metrics = []
    for attempt in range(len(os.listdir(f"HumanSolutions/problem{prob_num}"))):
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
        if functionality.valid_file(k_file) and functionality.can_file_pass(k_file, prob_num):
            # Add Halstead and mccabe metric scores to dict
            for key, value in Analyzer.HalsteadMetrics(k_file).metrics.items():
                metrics[key] = value
            metrics["MccabeComplexity"] = mccabe.get_total_value(k_file)
        all_metrics.append(metrics)

    return all_metrics








def innit_csv(csv_path: str, headers: list) -> None:
    """
    Sets up headers for Sample Score CSV Data
    :param csv_path: Path for the csv path to be written too
    :param headers:
    :return:
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
        # Reduces the impact of lots of code
        elif key == "EstProgLength" or  "Effort":
            sample_sum += (value / 10)
        else:
            sample_sum += value
    return sample_sum


def clear_file(file_path) -> None:
    """
    Clears the
    :return:
    """
    open(file_path, 'w').close()

def number_of_valid_solutions(file_path: str, k_iterations: int):
    """
    Gets how many valid python files are in the file path folder
    :param file_path: Path to solution folder
    :param k_iterations: Number of attempts
    :return: Number of valid files
    """
    valid = 0
    for attempt in range(k_iterations):
        k_file = f"{file_path}{attempt}.py"
        if functionality.valid_file(k_file):
            valid += 1
    return valid

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
