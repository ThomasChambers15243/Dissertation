import os
from dotenv import load_dotenv

load_dotenv()

''' ADD API KEY HERE '''
API_KEY = os.getenv('API_KEY')

# Initialize Research Parameters
STUDY_PARAMS = {
    "SAMPLE_RESULTS_CSV_FILE_PATH": "Code/data/SampleResults.csv",
    "HUMAN_RAW_RESULTS_CSV_FILE_PATH": "Code/data/RawHumanResults.csv",
    "GEN_RAW_RESULTS_CSV_FILE_PATH": "Code/data/RawGenResults.csv",
    "HUMAN_RESULTS_CSV_FILE_PATH": "Code/data/HumanResults.csv",
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
    "LOG_TESTING": f"{ROOT_DIR}Logs/SystemUnitTests.log",
    "LOG_GENERATION_RESPONSES": f"{ROOT_DIR}Logs/GenerationResponses.log"
}
