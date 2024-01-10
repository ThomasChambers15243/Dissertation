from Code import Analyzer
from Code import Generation
from Code import functionality
import csv
import json
import os



'''
Class to Gather all data from the samples
Write the human and generated data to csv
'''


class Gather:
    def __init__(self, params):
        # File Paths
        self.SAMPLE_RESULTS_CSV_FILE_PATH = params["SAMPLE_RESULTS_CSV_FILE_PATH"]
        self.RAW_RESULTS_CSV_FILE_PATH = params["RAW_RESULTS_CSV_FILE_PATH"]
        self.HUMAN_RESULTS_CSV_FILE_PATH = params["HUMAN_RESULTS_CSV_FILE_PATH"]
        self.GPT_SOLUTIONS_FILE_PATH = params["GPT_SOLUTIONS_FILE_PATH"]
        self.HUMAN_SOLUTIONS_FILE_PATH = params["HUMAN_SOLUTIONS_FILE_PATH"]
        self.PROBLEMS = json.load(open(params["PROBLEMS_FILE_PATH"]))

        # Research Parameters
        self.PROBLEM_AMOUNT = params["PROBLEM_AMOUNT"]
        self.TEMPERATURE_RANGES = params["TEMPERATURE_RANGES"]
        self.k_iterations = params["K_ITERATIONS"]

        # Research Outputs
        self.sampleScore = {}

    ''' 
    Gathers data for Generated responses
    '''

    def GetGPTData(self, temperature):
        # Sets up csv's headers
        self.__InnitCSV(self.SAMPLE_RESULTS_CSV_FILE_PATH, ["Problem", "Generation Amount", "Score"])

        # Remove any files from solutions
        self.__InnitSolutionsFolder()

        # Passed Count used in pass@k
        # failed = k_iterations - passed
        passed = 0

        # Generate GeneratedSolutions to problems at given temperature,
        for problemNumber, problem in enumerate(self.PROBLEMS):
            self.__GenerateSolutions(self.TEMPERATURE_RANGES[temperature], problemNumber, problem)

            # Tests Functionality of the Code - to be abstracted into method
            source = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--n"
            passed += functionality.TestFunctionality(source, problemNumber, self.k_iterations)

            # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
            filePath = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--"
            self.__CollectMetrics(problem, filePath)

        print(f"Pass@K: {functionality.passAtk(self.k_iterations*self.PROBLEM_AMOUNT, passed, self.k_iterations)}")

        # Write metric score to csv
        self.__WriteResults(self.SAMPLE_RESULTS_CSV_FILE_PATH, "gen")

    ''' 
    Gathers data for Human responses
    '''

    def GetHumanData(self):
        self.__InnitCSV(self.HUMAN_RESULTS_CSV_FILE_PATH, ["Problem", "Score"])

        # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
        for problemNumber, problem in enumerate(self.PROBLEMS):
            filePath = f"{self.HUMAN_SOLUTIONS_FILE_PATH}problem{problemNumber}/human--"
            self.__CollectMetrics(problem, filePath)

        # Write metric score to csv
        self.__WriteResults(self.HUMAN_RESULTS_CSV_FILE_PATH, "human")

    '''
    Collects metrics from the problem folder
    '''
    def __CollectMetrics(self, problem, filePath):
        # Calculate pass@K here

        # Calculate average scores and write them to a csv for each sample/problem
        # Sum all metrics for each solution
        totalSumMetrics = self.__SumMetricScores(filePath)

        # Calculate average metric
        totalSumMetrics = self.__CalculateAverageMetric(totalSumMetrics)

        # Total up all scores to produce one value
        self.sampleScore[problem] = self.__CalculateSampleScore(totalSumMetrics)

    '''
    Wipes any previous generations in solutions
    '''
    def __InnitSolutionsFolder(self):
        # Checks if the folder exists, if so, wipes the contents so the study starts anew
        for i in range(self.PROBLEM_AMOUNT):
            if os.path.exists(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}"):
                # Wipe content of folder
                for file in os.listdir(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}"):
                    os.remove(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}/{file}")
            else:
                # Create the folder
                os.mkdir(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}")

    '''
    Sets up headers for Sample Score CSV Data
    '''
    def __InnitCSV(self, csvPath, headers):
        # Create CSV File with appropriate headers
        with open(f"{csvPath}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    '''
    Generated GeneratedSolutions k number of times for the 
    given problem and temperature
    '''
    def __GenerateSolutions(self, temperature, problemNumber, problem):
        for i in range(self.k_iterations):
            with open(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--n{i}.py", "w") as file:
                response = Generation.GetResponce(self.PROBLEMS[problem], temperature)
                file.write(response)

    '''
    Given a folder with solutions,
    returns one dictionary with the total
    metrics of each solution
    '''
    def __SumMetricScores(self, filePath):
        # Dictionary to hold the sum total of metrics
        totalMetrics = {
            "distinctOperatorCount": 0,
            "distinctOperandCount": 0,
            "totalOperatorCount": 0,
            "totalOperandCount": 0,
            "vocab": 0,
            "length": 0,
            "eProgLength": 0,
            "volume": 0,
            "difficulty": 0,
            "effort": 0,
            "time": 0,
            "bugsEstimate": 0}

        for i in range(self.k_iterations):
            metrics = self.__CalculateMetrics(f"{filePath}n{i}.py")

            # Add the metrics to the running total
            for key, values in metrics.items():
                totalMetrics[key] += values

        return totalMetrics

    '''
    Calculates average metric scores
    '''
    def __CalculateAverageMetric(self, totalMetrics):
        # Calculates the mean for each metric
        for key, values in totalMetrics.items():
            totalMetrics[key] = values / self.k_iterations
        return totalMetrics

    '''
    Given a code file, return the metric scores as a dictionary
    Returns a Dictionary
    '''
    def __CalculateMetrics(self, solutionFilePath):
        return Analyzer.CalculateAllHalsteadMetrics(solutionFilePath)

    '''
    Calculates one value from the entire metrics dictionary
    Needs to be updated with scoring weights
    '''
    def __CalculateSampleScore(self, metrics):
        # return sum(value for key, value in metrics.items()) % 100
        return sum(value for key, value in metrics.items())

    '''
    Writes the sample score to given csv file
    '''
    def __WriteResults(self, filePath, sampleType):
        with open(filePath, "a", newline='') as file:
            writer = csv.writer(file)
            # Write generation scores
            if sampleType == "gen":
                for key, value in self.sampleScore.items():
                    writer.writerow([key, self.k_iterations, value])
            # Writes human Scores
            else:
                for key, value in self.sampleScore.items():
                    writer.writerow([key, value])

    '''
    Writes the raw results to raw csv file
    '''
    def __WriteRawResults(self, problemNumber):
        # Raw Headers
        # ["Problem", "Distinct Operators", "Distinct Operands", "Total Operators", "Total Operands",
        #                              "Vocabulary", "Length", "Estimated Program Length", "Volume", "Difficulty", "Effort",
        #                              "Time", "Bugs Estimate"]
        with open(self.RAW_RESULTS_CSV_FILE_PATH, "a", newline=' ') as file:
            writer = csv.writer(file)
            writer.writerow([problemNumber,
                             round(problemNumber["distinctOperatorCount"], 2),
                             round(problemNumber["distinctOperandCount"], 2),
                             round(problemNumber["totalOperatorCount"], 2),
                             round(problemNumber["totalOperandCount"], 2),
                             round(problemNumber["vocab"], 2),
                             round(problemNumber["length"], 2),
                             round(problemNumber["eProgLength"], 2),
                             round(problemNumber["volume"], 2),
                             round(problemNumber["difficulty"], 2),
                             round(problemNumber["effort"], 2),
                             round(problemNumber["time"], 2),
                             round(problemNumber["bugsEstimate"], 2)])
