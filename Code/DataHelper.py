import csv


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
