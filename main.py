from Code.Gather import Gather


# Initialize Research Parameters
STUDY_PARAMS = {
"SAMPLE_RESULTS_CSV_FILE_PATH" : "Code/data/SampleResults.csv",
"RAW_RESULTS_CSV_FILE_PATH" : "Code/data/RawResults.csv",
"HUMAN_RESULTS_CSV_FILE_PATH" : "Code/data/HumanResults.csv",
"GPT_SOLUTIONS_FILE_PATH" : "Solutions/",
"HUMAN_SOLUTIONS_FILE_PATH" : "HumanSolutions/",
"PROBLEMS_FILE_PATH" : "Code/data/pilotProblems.json",
"PROBLEM_AMOUNT" : 5,
"TEMPERATURE_RANGES" : {"0.3" : 0.4, "0.6" : 0.6, "0.9" : 0.9},
"K_ITERATIONS" : 1
}

if __name__ == '__main__':
    # Set up instance for Study
    DataGather = Gather(STUDY_PARAMS)
    # Set desired temperature
    temperature = "0.6"

    # Collect data in csv files
    DataGather.GetGPTData(temperature)
    DataGather.GetHumanData(temperature)
