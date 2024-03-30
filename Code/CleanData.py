import os
import csv
from shutil import rmtree
from loguru import logger
from distutils.dir_util import copy_tree
from config import PATHS

# Innit Logger
logger.add(f"{PATHS['LOG_MAIN']}", level="INFO")


def clean_failed_solutions(back_up=True):
    """
    Removes all zero's (failed solutions) from human and
    generated .csv files using config PATHS.
    Backs up data by default and re-writes if cleaning
    fails
    :param back_up bool Backs up data before cleaning and re-writes data if
    method fails. True by default
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
            try:
                load_backup_data()
                delete_backup_data()
            except Exception as e:
                logger.error(f"Could not load backup data. Error: {e}")
        return False

    # Deletes backed-up data
    if back_up:
        delete_backup_data()


def backup_data() -> None:
    """
    Backs up data by loading data into
    backup dirs, using config PATHS. Overwrites existing data
    :return: None
    """
    copy_tree(PATHS["HUMAN_RESULTS_CSV_DIR_PATH"], f"{PATHS['HUMAN_DATA_BACKUP']}")
    copy_tree(PATHS["SAMPLE_RESULTS_CSV_DIR_PATH"], f"{PATHS['GEN_DATA_BACKUP']}")


def load_backup_data() -> None:
    """
    Loads backed up data into main data
    dir using config PATHS. Overwrites existing data
    :return: None
    """
    copy_tree(f"{PATHS['HUMAN_DATA_BACKUP']}", f"{PATHS['HUMAN_RESULTS_CSV_DIR_PATH']}")
    copy_tree(f"{PATHS['GEN_DATA_BACKUP']}", PATHS["SAMPLE_RESULTS_CSV_DIR_PATH"])


def delete_backup_data() -> None:
    """
    Deletes backed up data.
    Overwrites existing data
    :return: None
    """
    rmtree(f"{PATHS['HUMAN_DATA_BACKUP']}")
    rmtree(f"{PATHS['GEN_DATA_BACKUP']}")


def delete_lines(target: str):
    """
    Deletes the lines from human and gen csv's that have
    zeroed values
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
        write_lines(human_file_path, human_rows_to_keep)
        write_lines(gen_file_path, gen_rows_to_keep)
    return True


def write_lines(file: str, file_rows: list[str]) -> None:
    """
    Writes the provided list to the files.
    Overwrites the contents
    :param file: String, path to file to write too
    :param file_rows: List of string rows to write to the file
    :return: None
    """
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(file_rows)


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
                if row[-1] != 'NA']
