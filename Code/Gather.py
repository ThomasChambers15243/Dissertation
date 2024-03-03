from Code import Analyzer
from Code import Generation
from Code import functionality
from Code import mccabe
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
        self.HUMAN_RAW_RESULTS_CSV_FILE_PATH = params["HUMAN_RAW_RESULTS_CSV_FILE_PATH"]
        self.GEN_RAW_RESULTS_CSV_FILE_PATH = params["GEN_RAW_RESULTS_CSV_FILE_PATH"]
        self.HUMAN_RESULTS_CSV_FILE_PATH = params["HUMAN_RESULTS_CSV_FILE_PATH"]
        self.GPT_SOLUTIONS_FILE_PATH = params["GPT_SOLUTIONS_FILE_PATH"]
        self.HUMAN_SOLUTIONS_FILE_PATH = params["HUMAN_SOLUTIONS_FILE_PATH"]
        self.PROBLEMS = json.load(open(params["PROBLEMS_FILE_PATH"], encoding="utf8"))

        # Research Parameters
        self.collectionType = ""
        self.PROBLEM_AMOUNT = params["PROBLEM_AMOUNT"]
        self.TEMPERATURE = params["TEMPERATURE"]
        self.k_iterations = params["K_ITERATIONS"]

        # Research Outputs
        self.sampleScore = {}
        self.notVaild = 0


    ''' 
    Gathers data for Generated responses
    '''

    def GetGPTData(self, temperature):
        # Set Type
        self.collectionType = "gen"
        # Sets up csv's headers
        self.__InnitCSV(self.SAMPLE_RESULTS_CSV_FILE_PATH, ["Problem", "Solution Amount", "Not Valid", "Score"])
        self.__InnitRawCSV(self.GEN_RAW_RESULTS_CSV_FILE_PATH, [
            "Problem", "Solution Amount", "Not Valid", "Distinct Operators", "Distinct Operands", "Total Operators",
            "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
            "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"])

        # Remove any files from solutions
        self.__InnitSolutionsFolder()

        # Passed Count used in pass@k
        # failed = k_iterations - passed
        passed = 0

        # Generate GeneratedSolutions to problems at given temperature,
        for problemNumber, problem in enumerate(self.PROBLEMS):
            self.__GenerateSolutions(self.TEMPERATURE, problemNumber, problem)

            # Tests Functionality of the Code - to be abstracted into method
            source = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--n"
            passed += functionality.TestGenerationFunctionality(source, problemNumber, self.k_iterations)

            # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
            filePath = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--n"
            totalSumMetrics = self.__CollectMetrics(problem, filePath)
            self.__WriteRawResults(problemNumber, totalSumMetrics)

        # Example Pass@k
        # print(f"Pass@K: {functionality.passAtk((100 * 20), 50, 100)}")
        print(f"""Passed /{self.k_iterations * self.PROBLEM_AMOUNT}: {passed}."
              f"\nPass@K: {functionality.passAtk((self.k_iterations*self.PROBLEM_AMOUNT), passed, self.k_iterations)}
              \n""")
        print(f"Not Valid:{self.notVaild}")

        # Write metric score to csv
        self.__WriteResults(self.SAMPLE_RESULTS_CSV_FILE_PATH)

        # Reset methodTestFile
        self.clearTestWriteFile()

    ''' 
    Gathers data for Human responses
    '''
    def GetHumanData(self):
        # Set Type
        self.collectionType = "h"
        self.__InnitCSV(self.HUMAN_RESULTS_CSV_FILE_PATH, ["Problem", "Solution Amount", "Not Valid", "Score"])
        self.__InnitRawCSV(self.HUMAN_RAW_RESULTS_CSV_FILE_PATH, [
            "Problem", "Solution Amount", "Not Valid", "Distinct Operators", "Distinct Operands", "Total Operators",
            "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
            "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"])
        passed = 0

        # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
        for problemNumber, problem in enumerate(self.PROBLEMS):
            filePath = f"{self.HUMAN_SOLUTIONS_FILE_PATH}problem{problemNumber}/human--n"
            passed += functionality.TestHumanFunctionality(filePath, problemNumber)
            totalSumMetrics = self.__CollectMetrics(problem, filePath)
            self.__WriteRawResults(problemNumber, totalSumMetrics)

        print(f"""Passed /{self.k_iterations * self.PROBLEM_AMOUNT}: {passed}.
              \nNot Valid: {self.notVaild}""")
        # Write metric score to csv
        self.__WriteResults(self.HUMAN_RESULTS_CSV_FILE_PATH)

        # Reset methodTestFile
        self.clearTestWriteFile()
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

        return totalSumMetrics

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

    def __InnitRawCSV(self, csvPath, headers):
        with open(f"{csvPath}", "w",newline='') as file:
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
                # Clean file from ```python & ``` comments in file
                response = response.replace("```python", "")
                response = response.replace("```", "")
                file.write(response)

    '''
    Given a folder with solutions,
    returns one dictionary with the total
    metrics of each solution
    '''
    def __SumMetricScores(self, filePath):
        # Dictionary to hold the sum total of metrics
        totalMetrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 0,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 0,
            "Vocabulary": 0,
            "Length": 0,
            "EstProgLength": 0,
            "Volume": 0,
            "Difficulty": 0,
            "Effort": 0,
            "Time": 0,
            "BugsEstimate": 0,
            "MccabeComplexity": 0}

        for attempt in range(self.k_iterations):
            kFile = f"{filePath}{attempt}.py"
            # Only add valid python files
            if not functionality.validFile(kFile):
                self.notVaild += 1
                continue
            # Add Halstead and mccabe metric scores
            for key, values in Analyzer.HalsteadMetrics(kFile).Metrics.items():
                totalMetrics[key] += values
            totalMetrics["MccabeComplexity"] = mccabe.GetTotalValue(kFile)
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
    Calculates one value from the entire metrics dictionary
    Needs to be updated with scoring weights
    '''
    def __CalculateSampleScore(self, metrics):
        # return sum(value for key, value in metrics.items()) % 100
        # print(metrics)
        return sum(value for key, value in metrics.items())

    '''
    Writes the sample score to given csv file
    '''
    def __WriteResults(self, filePath):
        with open(filePath, "a", newline='') as file:
            writer = csv.writer(file)
            # Write Scores
            for key, value in self.sampleScore.items():
                writer.writerow([key, self.k_iterations, round(value, 2)])


    '''
    Writes the raw results to raw csv file
    '''
    def __WriteRawResults(self, probNumber, metrics):
        # Raw Headers
        # ["Problem", "Solution Amount", "Distinct Operators", "Distinct Operands", "Total Operators",
        #     "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
        #     "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        if self.collectionType == "gen":
            path = self.GEN_RAW_RESULTS_CSV_FILE_PATH
        else:
            path = self.HUMAN_RAW_RESULTS_CSV_FILE_PATH
        with open(path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                            probNumber,
                            self.k_iterations,
                            self.notVaild,
                            round(metrics["DistinctOperatorCount"], 2),
                            round(metrics["DistinctOperandCount"], 2),
                            round(metrics["TotalOperatorCount"], 2),
                            round(metrics["TotalOperandCount"], 2),
                            round(metrics["Vocabulary"], 2),
                            round(metrics["Length"], 2),
                            round(metrics["EstProgLength"], 2),
                            round(metrics["Volume"], 2),
                            round(metrics["Difficulty"], 2),
                            round(metrics["Effort"], 2),
                            round(metrics["Time"], 2),
                            round(metrics["BugsEstimate"], 2),
                            round(metrics["MccabeComplexity"], 2)
                            ])

    def clearTestWriteFile(self):
        open("Tests/MethodTestFile.py", 'w').close()
