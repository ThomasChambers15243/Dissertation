import csv
import json
import os
from config import MODEL
from Code import DataHelper
from Code import Generation
from Code import functionality
from loguru import logger
from tqdm import tqdm

"""
Class to Gather all data from the samples
Write the human and generated data to csv
"""


class Gather:
    def __init__(self, params):
        ### File Paths ###
        # csv paths
        self.SAMPLE_RESULTS_CSV_DIR_PATH = params["SAMPLE_RESULTS_CSV_DIR_PATH"]
        self.RAW_SAMPLE_RESULTS_CSV_DIR_PATH = params["RAW_SAMPLE_RESULTS_CSV_DIR_PATH"]
        self.HUMAN_RESULTS_CSV_DIR_PATH = params["HUMAN_RESULTS_CSV_DIR_PATH"]
        self.RAW_HUMAN_RESULTS_CSV_DIR_PATH = params["RAW_HUMAN_RESULTS_CSV_DIR_PATH"]
        # Code Paths
        self.GPT_SOLUTIONS_FILE_PATH = params["GPT_SOLUTIONS_FILE_PATH"]
        self.HUMAN_SOLUTIONS_FILE_PATH = params["HUMAN_SOLUTIONS_FILE_PATH"]
        self.PROBLEMS = json.load(open(params["PROBLEMS_FILE_PATH"], encoding="utf8"))

        # Research Parameters
        self.collection_type = ""
        self.k_iterations = -1
        self.PROBLEM_AMOUNT = params["PROBLEM_AMOUNT"]
        self.TEMPERATURE = params["TEMPERATURE"]
        # Csv headers
        self.hum_csv_header = ["Attempt", "Score"]
        self.gen_csv_header = ["Attempt", "Temperature", "Score"]
        # Csv Raw headers
        self.raw_gen_csv_header = ["Attempt", "Temperature", "Distinct Operators", "Distinct Operands",
                                   "Total Operators",
                                   "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
                                   "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        self.raw_hum_csv_header = ["Attempt", "Distinct Operators", "Distinct Operands", "Total Operators",
                                   "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume",
                                   "Difficulty", "Effort", "Time", "Bugs Estimate", "Mccabe Complexity"]
        # Research Outputs
        self.sample_score = {}
        self.avg_sample_score = {}
        self.not_valid = 0
        self.total_passed = 0
        self.pass_at_ks = [0, 0, 0, 0, 0]

    def generate_gpt_solution(self, k_iterations):
        """
        Generates and saves gpt solutions
        :return: None
        """
        self.k_iterations = k_iterations
        # UNCOMMENT (just dont want to loose the 100 generations, it literally costs me money)
        # Clean solution folders
        # self._innit_solutions_folder()

        # Generate GeneratedSolutions to problems at given temperature
        # self._generate_solutions()

        # Records what the files are
        # self._save_generation_params()

    def get_gpt_data(self) -> None:
        """
        Gathers metric data for generated code and write results to csv and log files
        :return None
        """
        # Set Type
        self.collection_type = "gen"

        # Load data about the generated solutions
        saved_data = self._load_save_param_data()
        self.k_iterations = saved_data["k_iterations"]
        self.TEMPERATURE = saved_data["temperature"]

        # Collects daa for given solutions
        for problem_number, problem in tqdm(enumerate(self.PROBLEMS),
                                            total=self.PROBLEM_AMOUNT,
                                            desc="\033[34mCollecting Metric Data",
                                            ncols=100):
            # File path for the problem solution file
            file_path = f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}"
            # Checks there is a correct amount of solution in each folder
            # to the saved K value
            num_of_solutions = len(os.listdir(file_path))
            if num_of_solutions != self.k_iterations:
                logger.error(f"Num of attempts in dir {problem_number} is not equal to expected:"
                             f"{num_of_solutions} != k{self.k_iterations}")
            file_path += "/generated--n"

            # Gets metrics for problem
            metrics = DataHelper.get_metrics(problem_number, num_of_solutions, file_path)
            all_metrics, in_valid, passed = metrics[0], metrics[1], metrics[2]
            self.not_valid += in_valid
            self.total_passed += passed

            # Write Results
            self.write_results(all_metrics, problem_number)
            self.write_raw_results(all_metrics, problem_number)

            # Calculate pass@k for each problem
            self.pass_at_ks[problem_number] = functionality.pass_atk(self.k_iterations, passed, self.PROBLEM_AMOUNT)

        # Calculate Result Values
        total_samples = self.k_iterations * self.PROBLEM_AMOUNT
        total_pass_at_k = functionality.pass_atk(total_samples, self.total_passed, self.k_iterations)
        average_pass_at_k = sum(self.pass_at_ks) / self.PROBLEM_AMOUNT

        # Log Results
        results = f"""Generation Collection Results:
Model: {saved_data['model']}
Temperature: {saved_data['temperature']}
Total: {total_samples}.
Successful: {self.total_passed}.
Not Valid: {self.not_valid}.
Total Pass@{self.k_iterations}: {total_pass_at_k}
Average Pass@{self.k_iterations} per question: {average_pass_at_k}
Pass@{self.k_iterations} Values:
  Q1: {self.pass_at_ks[0]}
  Q2: {self.pass_at_ks[1]}
  Q3: {self.pass_at_ks[2]}
  Q4: {self.pass_at_ks[3]}
  Q5: {self.pass_at_ks[4]}"""
        logger.log("Results", results)
        logger.success(results)

        # Reset methodTestFile
        DataHelper.clear_file("Tests/MethodTestFile.py")

    def get_human_data(self) -> None:
        """
        Gather human data and write results to csv and logs files
        :return None
        """
        # Set Type
        self.collection_type = "h"
        num_of_solutions = -1
        # Collects the GeneratedSolutions metrics and stores them in self.sampleScore["problem"]
        for problem_number, problem in tqdm(enumerate(self.PROBLEMS),
                                            total=self.PROBLEM_AMOUNT,
                                            desc="\033[34mCollecting Metric Data",
                                            ncols=100):
            # File path for the problem solution file
            file_path = f"{self.HUMAN_SOLUTIONS_FILE_PATH}problem{problem_number}"
            num_of_solutions = len(os.listdir(file_path))
            file_path += "/human--n"

            # Gets metrics for problem
            metrics = DataHelper.get_metrics(problem_number, num_of_solutions, file_path)
            all_metrics, in_valid, passed = metrics[0], metrics[1], metrics[2]
            self.not_valid += in_valid
            self.total_passed += passed

            # Write Results
            self.write_results(all_metrics, problem_number)
            self.write_raw_results(all_metrics, problem_number)

        # Log results
        total_samples = num_of_solutions * self.PROBLEM_AMOUNT
        results = f"""Human Collection Results:
Total: {total_samples}.
Successful: {self.total_passed}.
Not Valid: {self.not_valid}"""
        logger.log("Results", results)
        logger.success(results)

        # Reset methodTestFile
        DataHelper.clear_file("Tests/MethodTestFile.py")

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

    def _generate_solutions(self) -> None:
        """
        Generated GeneratedSolutions k number of times for all problems,
        at the given temperature
        :return: None
        """
        # tqdm implements a progress bar [https://github.com/tqdm/tqdm] MIT liscance
        for problem_number, problem in tqdm(enumerate(self.PROBLEMS),
                                            total=self.PROBLEM_AMOUNT,
                                            desc="\033[34mGenerating Solutions For All Problems",
                                            ncols=100):
            for i in tqdm(range(self.k_iterations),
                          desc=f"\033[33mCurrent Problem: {problem}",
                          ncols=80,
                          leave=False):
                with open(f"{self.GPT_SOLUTIONS_FILE_PATH}problem{problem_number}/generated--n{i}.py", "w") as file:
                    response = Generation.get_response(self.PROBLEMS[problem], self.TEMPERATURE)

                    # Clean file from ```python & ``` comments in file
                    # A common occurrence in generation where otherwise the code would
                    # Be valid Python
                    response = response.replace("```python", "")
                    response = response.replace("```", "")
                    file.write(response)

    def _save_generation_params(self):
        """
        Save the generation data to a json file
        :return: None
        """
        # Data to save
        save_data = {
            "k_iterations": self.k_iterations,
            "temperature": self.TEMPERATURE,
            "problem_Amount": self.PROBLEM_AMOUNT,
            "model": MODEL
        }
        # Dumps save_data into a json file in the same dir as generated solutions
        try:
            with open(f"{self.GPT_SOLUTIONS_FILE_PATH}/genParms.json", "w") as save_file:
                json.dump(save_data, save_file)
            logger.success("Data Saved")
        except Exception as e:
            logger.error(f"Data could not be saved. Error: {e}")

    def _load_save_param_data(self) -> dict:
        """
        Gets the param data of the dataset
        :return: Dictionary of saved param data
        """
        try:
            with open(f"{self.GPT_SOLUTIONS_FILE_PATH}/genParms.json", "r") as save_file:
                save_data = json.load(save_file)
            return save_data
        except Exception as e:
            logger.error(f"Could not load saved param data. Error: {e}")

    def write_results(self, all_metrics: list[dict], prob_num: int) -> None:
        """
        Writes all metric scores to a csv file
        :param all_metrics: List of dic's of metrics for each solution in a problem
        :param prob_num: The problem that the metrics are for
        """
        # Sum Results
        all_metrics = [DataHelper.calculate_sample_score(solution) for solution in all_metrics]

        # Innit CSV header for gen or human solutions
        if self.collection_type == "gen":
            file_path = f"{self.SAMPLE_RESULTS_CSV_DIR_PATH}P{prob_num}.csv"
            DataHelper.innit_csv(file_path, self.gen_csv_header)
        else:
            file_path = f"{self.HUMAN_RESULTS_CSV_DIR_PATH}P{prob_num}.csv"
            DataHelper.innit_csv(file_path, self.hum_csv_header)

        # Two options as the headers for generated and human solutions
        # are slightly different, gen has 'temperature'
        with open(file_path, "a", newline='') as file:
            writer = csv.writer(file)
            # Write Scores
            for attempt in range(len(all_metrics)):
                if self.collection_type == "gen":
                    writer.writerow([attempt, self.TEMPERATURE, all_metrics[attempt]])
                else:
                    writer.writerow([attempt, all_metrics[attempt]])

    def write_raw_results(self, all_metrics: list[dict], prob_num: int) -> None:
        """
        Writes all metric values to a csv
        :param all_metrics: List of dic's of metrics for each solution in a problem
        :param prob_num: The problem that the metrics are for
        :return: None
        """
        # Innit csv header for gen and human
        if self.collection_type == "gen":
            file_path = f"{self.RAW_SAMPLE_RESULTS_CSV_DIR_PATH}P{prob_num}.csv"
            DataHelper.innit_csv(file_path, self.raw_gen_csv_header)
        else:
            file_path = f"{self.RAW_HUMAN_RESULTS_CSV_DIR_PATH}P{prob_num}.csv"
            DataHelper.innit_csv(file_path, self.raw_hum_csv_header)

        # Two options as the headers for generated and human solutions
        # are slightly different, gen has 'temperature'
        with open(file_path, "a", newline='') as file:
            writer = csv.writer(file)
            for attempt, metrics in enumerate(all_metrics):
                if self.collection_type == "gen":
                    writer.writerow([
                        attempt,
                        self.TEMPERATURE,
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
                else:
                    writer.writerow([
                        attempt,
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
