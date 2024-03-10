from Code import Analyzer
from Code import Generation
from Code import functionality
from Code import mccabe
from config import PATHS
from loguru import logger
import csv
import json
import os

# Init Logger
#logger.add(sink=PATHS['LOG_RESULTS'], level="INFO")

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
        self.rawCSVHeaders = ["Problem", "Solution Amount", "Not Valid", "Distinct Operators", "Distinct Operands",
                              "Total Operators",
                              "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
                              "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        self.csvHeaders = ["Problem", "Solution Amount", "Not Valid", "Score"]

        # Research Outputs
        self.sample_score = {}
        self.not_vaild = 0
        self.pass_at_ks = [0, 0, 0, 0, 0]


    def GetGPTData(self, temperature):
        """
        Gathers generation data
        :param temperature:
        :return:
        """
        # Set Type
        self.collectionType = "gen"
        # Sets up csv's headers
        self.__InnitCSV(self.SAMPLE_RESULTS_CSV_FILE_PATH, self.csvHeaders)
        self.__InnitCSV(self.GEN_RAW_RESULTS_CSV_FILE_PATH, self.rawCSVHeaders)

        # Remove any files from solutions
        self.__InnitSolutionsFolder()

        # Passed Count used in pass@k
        # failed = k_iterations - passed
        total_passed = 0

        # Generate GeneratedSolutions to problems at given temperature,
        for problem_number, problem in enumerate(self.PROBLEMS):
            self.__GenerateSolutions(self.TEMPERATURE, problem_number, problem)

            # Tests Functionality of the Code - to be abstracted into method
            source = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n"

            passed = functionality.TestGenerationFunctionality(source, problem_number, self.k_iterations)
            total_passed += passed

            # Calculate pass@k for each problem
            self.pass_at_ks[problem_number] = functionality.passAtk(self.k_iterations, passed, self.k_iterations)

            # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
            file_path = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n"
            total_sum_metrics = self.__CollectMetrics(problem, file_path)
            self.__WriteRawResults(problem_number, total_sum_metrics)

        # Write metric score to csv
        self.__WriteResults(self.SAMPLE_RESULTS_CSV_FILE_PATH)

        # Calculate results values
        total_samples = {self.k_iterations * self.PROBLEM_AMOUNT}
        # pass_k = functionality.passAtk((self.k_iterations * self.PROBLEM_AMOUNT), total_passed, self.k_iterations)
        average_pass_at_k = sum(self.pass_at_ks) / 5
        # Log results
        logger.log("Results", f"Generation Collection\n"
                          f"Total: {total_samples}.\n"
                          f"Successful: {total_passed}.\n"
                          f"Not Valid: {self.not_vaild}.\n"
                          f"Average Pass@k: {average_pass_at_k}\n"
                          f"Pass@k Values:\n"
                          f"    Q1: {self.pass_at_ks[0]}\n"
                          f"    Q2: {self.pass_at_ks[1]}\n"
                          f"    Q3: {self.pass_at_ks[2]}\n"
                          f"    Q4: {self.pass_at_ks[3]}\n"
                          f"    Q5: {self.pass_at_ks[4]}\n")

        # Reset methodTestFile
        self.clearTestWriteFile()


    def get_human_data(self):
        """
        Gather human data
        :return:
        """
        # Set Type
        self.collectionType = "h"
        self.__InnitCSV(self.HUMAN_RESULTS_CSV_FILE_PATH, self.csvHeaders)
        self.__InnitCSV(self.HUMAN_RAW_RESULTS_CSV_FILE_PATH, self.rawCSVHeaders)
        passed = 0

        # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
        for problemNumber, problem in enumerate(self.PROBLEMS):
            filePath = f"{self.HUMAN_SOLUTIONS_FILE_PATH}problem{problemNumber}/human--n"
            passed += functionality.TestHumanFunctionality(filePath, problemNumber)
            totalSumMetrics = self.__CollectMetrics(problem, filePath)
            self.__WriteRawResults(problemNumber, totalSumMetrics)

        # Write metric score to csv
        self.__WriteResults(self.HUMAN_RESULTS_CSV_FILE_PATH)

        # Log results
        totalSamples = self.k_iterations * self.PROBLEM_AMOUNT
        logger.log("Results", f"Human Collection.\n"
                          f"Total: {totalSamples}.\n"
                          f"Successful: {passed}.\n"
                          f"Not Valid: {self.not_vaild}\n")

        # Reset methodTestFile
        self.clearTestWriteFile()


    def __CollectMetrics(self, problem, filePath):
        """
        Collect metrics from the problem folder
        """
        # Calculate pass@K here

        # Calculate average scores and write them to a csv for each sample/problem
        # Sum all metrics for each solution
        totalSumMetrics = self.__SumMetricScores(filePath)

        # Calculate average metric
        totalSumMetrics = self.__CalculateAverageMetric(totalSumMetrics)

        # Total up all scores to produce one value
        self.sample_score[problem] = self.__CalculateSampleScore(totalSumMetrics)

        return totalSumMetrics


    def __InnitSolutionsFolder(self):
        """
        Wipes any previous generations in solutions
        :return:
        """
        # Checks if the folder exists, if so, wipes the contents so the study starts anew
        for i in range(self.PROBLEM_AMOUNT):
            if os.path.exists(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}"):
                # Wipe content of folder
                for file in os.listdir(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}"):
                    os.remove(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}/{file}")
            else:
                # Create the folder
                os.mkdir(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{i}")


    def __InnitCSV(self, csvPath, headers):
        """
        Sets up headers for Sample Score CSV Data
        :param csvPath:
        :param headers:
        :return:
        """
        # Create CSV File with appropriate headers
        with open(f"{csvPath}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)


    def __GenerateSolutions(self, temperature, problemNumber, problem):
        """
        Generated GeneratedSolutions k number of times for the
        given problem and temperature
        :param temperature:
        :param problemNumber:
        :param problem:
        :return:
        """
        for i in range(self.k_iterations):
            with open(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problemNumber}/generated--n{i}.py", "w") as file:
                response = Generation.GetResponce(self.PROBLEMS[problem], temperature)
                # Clean file from ```python & ``` comments in file
                response = response.replace("```python", "")
                response = response.replace("```", "")
                file.write(response)


    def __SumMetricScores(self, filePath):
        """
        Given a folder with solutions,
        returns one dictionary with the total
        metrics of each solution
        :param filePath:
        :return:
        """
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
                self.not_vaild += 1
                continue
            # Add Halstead and mccabe metric scores
            for key, values in Analyzer.HalsteadMetrics(kFile).Metrics.items():
                totalMetrics[key] += values
            totalMetrics["MccabeComplexity"] = mccabe.GetTotalValue(kFile)
        return totalMetrics


    def __CalculateAverageMetric(self, totalMetrics):
        """
        Calculates average metric scores
        :param totalMetrics:
        :return:
        """
        # Calculates the mean for each metric
        for key, values in totalMetrics.items():
            try:
                totalMetrics[key] = values / (self.k_iterations - self.not_vaild)
            except ZeroDivisionError:
                return totalMetrics
        return totalMetrics


    def __CalculateSampleScore(self, metrics):
        """
        Calculates one value from the entire metrics dictionary
        Needs to be updated with scoring weights
        :param metrics:
        :return:
        """
        sum = 0
        for key, value in metrics.items():
            # Increases impact of Mccabe
            if key == "MccabeComplexity":
                sum += (value * 100)
            # Reduces the impact of lots of code
            elif key == "EstProgLength" or "Effort":
                sum += (value / 10)
            else:
                sum += value
        return sum


    def __WriteResults(self, filePath):
        """
        Writes the sample score to given csv file
        :param filePath:
        :return:
        """
        with open(filePath, "a", newline='') as file:
            writer = csv.writer(file)
            # Write Scores
            for key, value in self.sample_score.items():
                writer.writerow([key, self.k_iterations, round(value, 2)])


    def __WriteRawResults(self, probNumber, metrics):
        """
        Writes the raw results to raw csv file
        :param probNumber:
        :param metrics:
        :return:
        """
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
                self.not_vaild,
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
