import Generation
import Analyzer
import csv
import json

# Create CSV File with appropriate headers
with open('results.csv', 'w', newline='') as file:
   writer = csv.writer(file)
   writer.writerow(["Problem", "Distinct Operators", "Distinct Operands", "Total Operators", "Total Operands", "Vocabulary", "Length", "Estimated Program Length", "Volume", "Difficulty", "Effort", "Time", "Bugs Estimate"])

# Initialize Research Parameters
problems = json.load(open('problems.json'))
problemAmount = 6
k = 1
temperature = 0.6

# Generate Solutions
pNumber = 1
for p in problems:
    for i in range(1, k+1):
        with open(f"Solutions/problem{pNumber}/p{pNumber}-{i}.py", "w") as file:
            response = Generation.GetResponce(problems[p], temperature)
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
    with open("results.csv", mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([solution, totalMetrics["distinctOperatorCount"], totalMetrics["distinctOperandCount"], totalMetrics["totalOperatorCount"], totalMetrics["totalOperandCount"], totalMetrics["vocab"], totalMetrics["length"], totalMetrics["eProgLength"], totalMetrics["volume"], totalMetrics["difficulty"], totalMetrics["effort"], totalMetrics["time"], totalMetrics["bugsEstimate"]])
