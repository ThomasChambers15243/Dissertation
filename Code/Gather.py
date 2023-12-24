import Analyzer
import Generation
import csv
import json
import os

class Gather:
    def __innit(self,
                RAW_RESULTS_CSV_FILE_PATH,
                SAMPLE_RESULTS_CSV_FILE_PATH,
                SOLUTIONS_FILE_PATH,
                PROBLEMS_FILE_PATH,
                PROBLEM_AMOUNT,
                TEMPERATURE_RANGES,
                k_iterations):
        # File Paths
        self.RAW_RESULTS_CSV_FILE_PATH = RAW_RESULTS_CSV_FILE_PATH
        self.SAMPLE_RESULTS_CSV_FILE_PATH = SAMPLE_RESULTS_CSV_FILE_PATH
        self.SOLUTIONS_FILE_PATH = SOLUTIONS_FILE_PATH
        self.PROBLEMS = json.load(open(PROBLEMS_FILE_PATH))

        # Research Parameters
        self.PROBLEM_AMOUNT = PROBLEM_AMOUNT        
        self.TEMPERATURE_RANGES = TEMPERATURE_RANGES
        self.k_iterations = k_iterations

        # Research Outputs
        self.metrics = {}

    # One method to gather all data from the proposed samples
    def GetData(self):
        for temperature in self.TEMPERATURE_RANGES:
            # Remove any files from solutions
            self.InnitSolutionsFolder()

            # Generate Solutions to problems at given temperature,
            # writing them to files
            self.GenerateSolutions(temperature)

            # Pass at K here

            # Calculate average scores and write them to a csv for each sample/problem
            for problemNumber, problem in enumerate(self.PROBLEMS):
                totalSumMetrics = self.SumMetricScores(f"{self.SOLUTIONS_FILE_PATH}problem{problemNumber}/")
                totalSumMetrics = self.CalculateAverageMetric(totalSumMetrics)

                # Write metric average to csv


        raise NotImplementedError


    # Cleans the Solutions Folder
    def InnitSolutionsFolder(self):
        # Checks if the folder exists, if so, wipes the contents so the study starts anew
        for i in range(self.PROBLEM_AMOUNT):
            if os.path.exists(f"{self.SOLUTIONS_FILE_PATH}problem{i}"):
                # Wipe content of folder
                for file in os.listdir(f"{self.SOLUTIONS_FILE_PATH}problem{i}"):
                    os.remove(f"{self.SOLUTIONS_FILE_PATH}problem{i}/{file}")
            else:
                # Create the folder
                os.mkdir(f"{self.SOLUTIONS_FILE_PATH}problem{i}")

    # Sets up headers for results .csv
    def InnitCSV(self, csvPath):
        # Create CSV File with appropriate headers
        with open(f"{csvPath}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Problem", "Distinct Operators", "Distinct Operands", "Total Operators", "Total Operands",
                             "Vocabulary", "Length", "Estimated Program Length", "Volume", "Difficulty", "Effort",
                             "Time", "Bugs Estimate"])

    # Generates solutions for all problems at
    # given temperature
    # given number of iterations
    def GenerateSolutions(self, temperature):
        for problemNumber, problem in enumerate(self.PROBLEMS):
            for i in range(self.k_iterations):
                with open(f"{self.SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--{i}.py", "w") as file:
                    response = Generation.GetResponce(self.PROBLEMS[problem], temperature)
                    file.write(response)

    # Given a folder with solutions,
    # returns one dictionary with the total
    # metrics of each solution
    def SumMetricScores(self, problemFolderPath):
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

        # For each Solution to that problem
        for i in range(self.k_iterations):
            metrics = self.CalculateMetrics(f"{problemFolderPath}generated--{i}.py")
            # Add the metrics to the running total
            for key, values in metrics.items():
                totalMetrics[key] += values

        return totalMetrics

    # Calculates average metric scores
    def CalculateAverageMetric(self, totalMetrics):
        # Calculates the mean for each metric
        for key, values in totalMetrics.items():
            totalMetrics[key] = values / self.k_iterations
        return totalMetrics


    # Given a code file, return the metric scores as a dictionary
    # Returns a Dictionary
    def CalculateMetrics(self, solutionFilePath):
        return Analyzer.CalculateAllHalsteadMetrics(solutionFilePath)

    def CalculateSampleScore(self):
        raise NotImplementedError

    def WriteRawResults(self,rawResultsFilePath):
        raise NotImplementedError

    def WriteSampleResults(self, sampleResultsFilePath):
        raise NotImplementedError

    def WriteResults(self):
        raise NotImplementedError