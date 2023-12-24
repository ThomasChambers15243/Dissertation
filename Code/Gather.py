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
        self.PROBLEMS_FILE_PATH = PROBLEMS_FILE_PATH

        # Research Parameters
        self.PROBLEM_AMOUNT = PROBLEM_AMOUNT        
        self.TEMPERATURE_RANGES = TEMPERATURE_RANGES
        self.k_iterations = k_iterations

        # Research Outputs
        self.metrics = {}

    # One method to gather all data from the proposed samples
    def GetData(self):
        raise NotImplementedError

    # Cleans the Solutions Folder
    def InnitSolutionsFolder(self):
        raise NotImplementedError

    # Generates solutions
    def GenerateSolutions(self, solutionsfilePath, desiredTemperature, numOfIterations):
        raise NotImplementedError

    # Given a code file, return the metric scores as a dictionary
    # Returns a Dictionary
    def CalculateMetric(self, solutionFilePath):
        raise NotImplementedError

    # Given a list of metric dictionary scores,
    # calculates the mean of each value.
    # Returns a dictionary

    def CalculateAverageMetric(self,solutionFilePath):
        raise NotImplementedError

    def CalculateSampleScore(self):
        raise NotImplementedError

    def WriteRawResults(self,rawResultsFilePath):
        raise NotImplementedError

    def WriteSampleResults(self, sampleResultsFilePath):
        raise NotImplementedError

    def WriteResults(self):
        raise NotImplementedError