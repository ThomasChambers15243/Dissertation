import os
import shutil
from config import PATHS
from loguru import logger

# Innit Logger
logger.add(f"{PATHS['LOG_MAIN']}", level="INFO")


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


if __name__ == "__main__":
    load_human_files()
