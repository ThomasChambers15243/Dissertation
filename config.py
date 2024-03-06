from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Research Parameters
STUDY_PARAMS = {
"SAMPLE_RESULTS_CSV_FILE_PATH" : "Code/data/SampleResults.csv",
"HUMAN_RAW_RESULTS_CSV_FILE_PATH" : "Code/data/RawHumanResults.csv",
"GEN_RAW_RESULTS_CSV_FILE_PATH" : "Code/data/RawGenResults.csv",
"HUMAN_RESULTS_CSV_FILE_PATH" : "Code/data/HumanResults.csv",
"GPT_SOLUTIONS_FILE_PATH" : "GeneratedSolutions/",
"HUMAN_SOLUTIONS_FILE_PATH" : "HumanSolutions/",
"PROBLEMS_FILE_PATH" : "Code/data/ProblemQuestions.json",
"PROBLEM_AMOUNT" : 5,
"TEMPERATURE": 0.6,
"K_ITERATIONS" : 1
}

''' ADD API KEY HERE '''
API_KEY = os.getenv('API_KEY')

# Old temperature method: "TEMPERATURE_RANGES" : {"0.3" : 0.4, "0.6" : 0.6, "0.9" : 0.9},