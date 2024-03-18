import csv
from Code import functionality

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
        elif key == "EstProgLength" or "Effort":
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
        if functionality.test_human_functionality(k_file, prob_num):
            passed += 1
    return passed
