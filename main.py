from Code.Gather import Gather



# Initialize Research Parameters
STUDY_PARAMS = {
"SampleResultsPath" : "Code/data/SampleResults.csv",
"RawResultsPath" : "Code/data/RawResults.csv",
"SolutionsPath" : "Solutions/",
"ProblemsPath" : "Code/data/pilotProblems.json",
"ProblemAmount" : 5,
"TemperatureRange" : [0.3, 0.6, 0.9],
"kIterations" : 1,
}

if __name__ == '__main__':
    DataGather = Gather(
        RAW_RESULTS_CSV_FILE_PATH=STUDY_PARAMS["SampleResultsPath"],
        SAMPLE_RESULTS_CSV_FILE_PATH=STUDY_PARAMS["RawResultsPath"],
        SOLUTIONS_FILE_PATH=STUDY_PARAMS["SolutionsPath"],
        PROBLEMS_FILE_PATH=STUDY_PARAMS["ProblemsPath"],
        PROBLEM_AMOUNT=STUDY_PARAMS["ProblemAmount"],
        TEMPERATURE_RANGES=STUDY_PARAMS["TemperatureRange"],
        k_iterations=STUDY_PARAMS["kIterations"])

    DataGather.GetData()