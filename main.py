import Generation
import Analyzer
import csv
import json
import os

# Create CSV File with appropriate headers
with open('results.csv', 'w', newline='') as file:
   writer = csv.writer(file)
   writer.writerow(["Problem", "Distinct Operators", "Distinct Operands", "Total Operators", "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume", "Difficulty", "Effort", "Time", "Bugs Estimate"])

# Checks if the folder exists, if so, wipes the contents so the study starts anew
for i in range(1, 7):
    if os.path.exists(f"Solutions/problem{i}"):
        for file in os.listdir(f"Solutions/problem{i}"):
            os.remove(f"Solutions/problem{i}/{file}")
    else:
        # Create the folder
        os.mkdir(f"Solutions/problem{i}")

# Initialize Research Parameters
problems = json.load(open('pilotProblems.json'))
problemAmount = 6
k = 1
temperature = [0.1, 1]
run = 1
while run < 2:
    # Generate Solutions
    pNumber = 1
    for p in problems:
        for i in range(1, k+1):
            with open(f"Solutions/problem{pNumber}/p{pNumber}-{i}.py", "w") as file:
                response = Generation.GetResponce(problems[p], temperature[run])
                print(f"temperature: {temperature[run]}")
                file.write(response)
        pNumber += 1



    # For each problem, calculate the  average metrics for each sample to the solution
    for solution in range(1, problemAmount+1):
        # Dictionary to hold the running total and average of the metrics
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
        for i in range(1, k+1):
            metrics = Analyzer.CalculateAllHalsteadMetrics(f"Solutions/problem{solution}/p{solution}-{i}.py")
            # Add the metrics to the running total
            for key, values in metrics.items():
                totalMetrics[key] += values

        # Average the metrics
        for key, values in totalMetrics.items():
            totalMetrics[key] = values / k

        # Write the average metrics to a csv file
        with open("results.csv", 'a', newline='') as file:
            print(f"Run: {run},")
            writer = csv.writer(file)
            writer.writerow([solution,
                             round(totalMetrics["distinctOperatorCount"], 2),
                             round(totalMetrics["distinctOperandCount"], 2),
                             round(totalMetrics["totalOperatorCount"], 2),
                             round(totalMetrics["totalOperandCount"], 2),
                             round(totalMetrics["vocab"], 2),
                             round(totalMetrics["length"], 2),
                             round(totalMetrics["eProgLength"], 2),
                             round(totalMetrics["volume"], 2),
                             round(totalMetrics["difficulty"], 2),
                             round(totalMetrics["effort"], 2),
                             round(totalMetrics["time"], 2),
                             round(totalMetrics["bugsEstimate"], 2)])
    # Add an emtpy line to results.csv
    with open("results.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])
    run += 1