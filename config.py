import os
import io
from dotenv import load_dotenv

load_dotenv()

# 'Nowhere' target for the text runner to print through,
# this avoids clogging up the console
NULL_STREAM = io.StringIO()

''' ADD API KEY HERE '''
API_KEY = os.getenv('API_KEY')

# Models
ACCEPTED_MODELS = ["gpt-3.5", "gpt-3.5-turbo"]
MODEL = "gpt-3.5-turbo"

# Initialize Research Parameters
STUDY_PARAMS = {
    "SAMPLE_RESULTS_CSV_DIR_PATH": "Code/data/SampleResults/",
    "HUMAN_RESULTS_CSV_DIR_PATH": "Code/data/HumanResults/",
    "RAW_SAMPLE_RESULTS_CSV_DIR_PATH": "Code/data/RawSampleResults/",
    "RAW_HUMAN_RESULTS_CSV_DIR_PATH": "Code/data/RawHumanResults/",
    "GPT_SOLUTIONS_FILE_PATH": "GeneratedSolutions/",
    "HUMAN_SOLUTIONS_FILE_PATH": "HumanSolutions/",
    "PROBLEMS_FILE_PATH": "Code/data/ProblemQuestions.json",
    "PROBLEM_AMOUNT": 5,
    "TEMPERATURE": 0.6,
    "K_ITERATIONS": 1
}

ROOT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/"

PATHS = {
    "ROOT_DIR": ROOT_DIR,
    "PYTHON_FILE_TEST_SAMPLES": f"{ROOT_DIR}Tests/TestFiles/PythonFileTestSamples/",
    "LOG_MAIN": f"{ROOT_DIR}Logs/Main.log",
    "LOG_RESULTS": f"{ROOT_DIR}Logs/Results.log",
    "LOG_TESTING": f"{ROOT_DIR}Logs/MainSystemTests.log",
    "LOG_GENERATION_RESPONSES": f"{ROOT_DIR}Logs/GenerationResponses.log",
    "METHOD_TEST_FILE": f"{ROOT_DIR}Tests/MethodTestFile.py"
}
