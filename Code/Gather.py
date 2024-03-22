import csv
import json
import os
from Code import DataHelper
from Code import Analyzer
from Code import Generation
from Code import functionality
from Code import mccabe
from loguru import logger

"""
Class to Gather all data from the samples
Write the human and generated data to csv
"""


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
        self.collection_type = ""
        self.PROBLEM_AMOUNT = params["PROBLEM_AMOUNT"]
        self.TEMPERATURE = params["TEMPERATURE"]
        self.k_iterations = params["K_ITERATIONS"]
        self.raw_csv_headers = ["Problem", "Solution Amount", "Not Valid", "Distinct Operators", "Distinct Operands",
                                "Total Operators",
                                "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
                                "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        self.csv_headers = ["Problem", "Solution Amount", "Not Valid", "Score"]

        # Research Outputs
        self.sample_score = {}
        self.not_valid = 0
        self.total_passed = 0
        self.pass_at_ks = [0, 0, 0, 0, 0]

    def get_gpt_data(self) -> None:
        """
        Gathers generation data and write results to csv and log files
        :return None
        """
        # Set Type
        self.collection_type = "gen"
        # Sets up csv's headers
        DataHelper.innit_csv(self.SAMPLE_RESULTS_CSV_FILE_PATH, self.csv_headers)
        DataHelper.innit_csv(self.GEN_RAW_RESULTS_CSV_FILE_PATH, self.raw_csv_headers)

        # Remove any files from solutions
        self._innit_solutions_folder()

        # Generate GeneratedSolutions to problems at given temperature,
        for problem_number, problem in enumerate(self.PROBLEMS):
            self._generate_solutions(self.TEMPERATURE, problem_number, problem)
            # File path for the problem solution file
            source = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n"
            # Tests functionality of all solutions
            #passed = functionality.test_generation_functionality(source, problem_number, self.k_iterations)
            passed = DataHelper.number_of_passed_solutions(source, self.k_iterations, problem_number)
            self.total_passed += passed

            # Calculate pass@k for each problem
            self.pass_at_ks[problem_number] = functionality.pass_atk(self.k_iterations, passed, self.k_iterations)

            # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
            file_path = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n"
            total_sum_metrics = self._collect_metrics(problem, file_path)
            self._write_raw_results(problem_number, total_sum_metrics)

        # Write metric score to csv
        self._write_results(self.SAMPLE_RESULTS_CSV_FILE_PATH)

        # Calculate results values
        total_samples = {self.k_iterations * self.PROBLEM_AMOUNT}
        average_pass_at_k = sum(self.pass_at_ks) / 5
        # Log results
        logger.log("Results", f"Generation Collection\n"
                              f"Total: {total_samples}.\n"
                              f"Successful: {self.total_passed}.\n"
                              f"Not Valid: {self.not_valid}.\n"
                              f"Average Pass@k: {average_pass_at_k}\n"
                              f"Pass@k Values:\n"
                              f"    Q1: {self.pass_at_ks[0]}\n"
                              f"    Q2: {self.pass_at_ks[1]}\n"
                              f"    Q3: {self.pass_at_ks[2]}\n"
                              f"    Q4: {self.pass_at_ks[3]}\n"
                              f"    Q5: {self.pass_at_ks[4]}\n")

        # Reset methodTestFile
        DataHelper.clear_file("Tests/MethodTestFile.py")

    def get_human_data(self) -> None:
        """
        Gather human data and write results to csv and logs files
        :return None
        """
        # Set Type
        self.collection_type = "h"
        DataHelper.innit_csv(self.HUMAN_RESULTS_CSV_FILE_PATH, self.csv_headers)
        DataHelper.innit_csv(self.HUMAN_RAW_RESULTS_CSV_FILE_PATH, self.raw_csv_headers)

        # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
        for problem_number, problem in enumerate(self.PROBLEMS):
            # File path for the problem solution file
            file_path = f"{self.HUMAN_SOLUTIONS_FILE_PATH}problem{problem_number}/human--n"
            # Tests the functionality and validity of the solutions
            self.is_valid = DataHelper.number_of_valid_solutions(file_path, self.k_iterations)
            self.total_passed += DataHelper.number_of_passed_solutions(file_path, self.k_iterations, problem_number)

            total_sum_metrics = self._collect_metrics(problem_number, file_path)
            self._write_raw_results(problem_number, total_sum_metrics)

        # Write metric score to csv
        self._write_results(self.HUMAN_RESULTS_CSV_FILE_PATH)

        # Log results
        total_samples = self.k_iterations * self.PROBLEM_AMOUNT
        logger.log("Results", f"Human Collection.\n"
                              f"Total: {total_samples}.\n"
                              f"Successful: {self.total_passed}.\n"
                              f"Not Valid: {self.not_valid}\n")

        # Reset methodTestFile
        DataHelper.clear_file("Tests/MethodTestFile.py")

    def _collect_metrics(self, problem_number: int, file_path: str) -> dict:
        """
        Collect metrics from the problem folder
        :param Problem in form p{b}
        :return Dict of metrics with each sum metric for each solution
        """

        # Sum all metrics for each solution
        total_sum_metrics = self._sum_metric_scores(problem_number, file_path)

        # Calculate average metric
        total_sum_metrics = self._calculate_average_metric(total_sum_metrics)

        # Total up all scores to produce one value
        self.sample_score[f"P{problem_number}"] = DataHelper.calculate_sample_score(total_sum_metrics)

        return total_sum_metrics

    def _innit_solutions_folder(self) -> None:
        """
        Wipes any previous generations in solutions
        :return None
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

    def _generate_solutions(self, temperature: float, problem_number: int, problem: str) -> None:
        """
        Generated GeneratedSolutions k number of times for the
        given problem and temperature
        :param temperature: Temperature for model to use in generation
        :param problem_number: Problem number
        :param problem: Problem as p{n} form
        :return: None
        """
        for i in range(self.k_iterations):
            with open(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n{i}.py", "w") as file:
                response = Generation.get_response(self.PROBLEMS[problem], temperature)

                # Clean file from ```python & ``` comments in file
                # A common occurrence in generation where otherwise the code would
                # Be valid Python
                response = response.replace("```python", "")
                response = response.replace("```", "")
                file.write(response)

    def _sum_metric_scores(self, prob_num: int, file_path: str) -> dict:
        """
        Given a folder with solutions,
        returns one dictionary with the total
        metrics of each solution
        :param file_path: String file path to get scores from
        :return Dict containing the total Halstead scores of each solution
        """
        # Dictionary to hold the sum total of metrics
        total_metrics = {
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
            k_file = f"{file_path}{attempt}.py"
            # Only add valid files which passed
            if not functionality.valid_file(k_file) and functionality.can_file_pass(k_file, prob_num):
                continue
            # Add Halstead and mccabe metric scores
            for key, values in Analyzer.HalsteadMetrics(k_file).metrics.items():
                total_metrics[key] += values
            total_metrics["MccabeComplexity"] = mccabe.get_total_value(k_file)
        return total_metrics

    # TODO
    #   Don't count metrics from non successful submission
    def _calculate_average_metric(self, total_metrics: dict) -> dict:
        """
        Calculates average metric scores
        :param total_metrics: Dict of Halstead scores
        :return: Dict of each average Halstead score for all solutions
        """
        # Calculates the mean for each metric
        for key, values in total_metrics.items():
            try:
                total_metrics[key] = values / (self.k_iterations - self.not_valid)
            except ZeroDivisionError:
                return total_metrics
        return total_metrics

    def _write_results(self, file_path: str) -> None:
        """
        Writes the sample score to given csv file
        :param file_path: File path to write
        :return: None
        """
        with open(file_path, "a", newline='') as file:
            writer = csv.writer(file)

            # Write Scores
            for key, value in self.sample_score.items():
                writer.writerow([key, self.k_iterations, round(value, 2)])

    def _write_raw_results(self, prob_number: int, metrics: dict) -> None:
        """
        Writes the raw results to raw csv file
        :param prob_number: The problem number relevant to the metric scores
        :param metrics: Metrics Halstead scores to write to the csv
        :return: None
        """
        # Raw Headers
        # ["Problem", "Solution Amount", "Distinct Operators", "Distinct Operands", "Total Operators",
        #     "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
        #     "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        if self.collection_type == "gen":
            path = self.GEN_RAW_RESULTS_CSV_FILE_PATH
        else:
            path = self.HUMAN_RAW_RESULTS_CSV_FILE_PATH
        with open(path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                prob_number,
                self.k_iterations,
                self.not_valid,
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
