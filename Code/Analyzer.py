import math
from Code import Lexer
# File for analyzing code and Performing Halstead Calculations

# Halstead Calculations
#
# n1 = the number of distinct operators
# n2 = the number of distinct operands
# N1 = the total number of operators
# N2 = the total number of operands
#
# Program vocabulary: n = n1 + n2
# Program length: N = N1 + N2
# Calculated program length: N'=n1log2(n1)+n2log2(n2)
# Volume: V= Nlog2(n)
# Difficulty: D= (n1/2) * (N2/n2)
# Effort: E= DV

# Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
# Operands are variables, methods, constants (False, True, strings and other data type values)




# DistinctOperatorCount,distinctOperandCount,totalOperatorCount,totalOperandCount
# n1                    n2                 N1                   N2
def ShowOperatorAndOperandStats(sourceCodeFilePath):
    # Tokenize the code and get the metrics
    operators, operands = Lexer.TokeniseCode(sourceCodeFilePath)

    # Acquires the Halstead metrics as n1, n2, N1, N2
    distinctOperatorCount = len(operators[1])
    distinctOperandCount = len(operands[1])
    totalOperatorCount = operators[0]
    totalOperandCount = operands[0]

    # Prints out above counts
    print(f"Number of Distinct Operators: {distinctOperatorCount}\n")
    print(f"Number of Distinct Operands: {distinctOperandCount}\n")
    print(f"Total Number of Operators: {totalOperatorCount}\n")
    print(f"Total Number of Operands: {totalOperandCount}\n")

def Vocabulary(distinctOperatorCount, distinctOperandCount):
    return distinctOperatorCount + distinctOperandCount

def Length(totalOperatorCount, totalOperandCount):
    return totalOperatorCount + totalOperandCount

def EstimatedProgramLength(distinctOperatorCount, distinctOperandCount):
    try:
        lhs = distinctOperatorCount * math.log2(distinctOperatorCount)
        rhs = distinctOperandCount * math.log2(distinctOperandCount)
    except ValueError:
        return 0
    return lhs + rhs

def Volume(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount):
    try:
        Volume = Length(totalOperatorCount, totalOperandCount) * math.log2(
        Vocabulary(distinctOperatorCount, distinctOperandCount))
        return Volume
    except ValueError:
        return 0

def Difficulty(distinctOperatorCount, distinctOperandCount, totalOperandCount):
    return (distinctOperatorCount / 2) * (totalOperandCount / distinctOperandCount)

def Effort(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount, difficulty=None, volume=None):
    if difficulty is None or volume is None:
        return Difficulty(distinctOperatorCount, distinctOperandCount, totalOperandCount) * Volume(totalOperatorCount, totalOperandCount, distinctOperatorCount)
    return difficulty * volume

def Time(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount, effort=None):
    if effort is None:
        effort = Effort(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount)
    return effort / 18

def BugsEstimate(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount,volume=None):
    if volume is None:
        return Volume(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount) / 3000
    return volume / 3000

# Calculates all Halstead Metrics and returns them as a dictionary
def CalculateAllHalsteadMetrics(sourceCodeFilePath):
    # Tokenize the code and get the metrics
    operators, operands = Lexer.TokeniseCode(sourceCodeFilePath)

    # Acquires the Halstead metrics as n1, n2, N1, N2
    distinctOperatorCount = len(operators[1])
    distinctOperandCount = len(operands[1])
    totalOperatorCount = operators[0]
    totalOperandCount = operands[0]

    # Calculate Metrics
    vocabulary = Vocabulary(distinctOperatorCount, distinctOperandCount)
    length = Length(totalOperatorCount, totalOperandCount)
    estimatedProgramLength = EstimatedProgramLength(distinctOperatorCount, distinctOperandCount)
    volume = Volume(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount)
    difficulty = Difficulty(distinctOperatorCount, distinctOperandCount, totalOperandCount)
    effort = Effort(totalOperatorCount,totalOperandCount, distinctOperatorCount, distinctOperandCount, difficulty, volume)
    time = Time(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount, effort)
    bugsEstimate = BugsEstimate(totalOperatorCount, totalOperandCount, distinctOperatorCount,distinctOperandCount, volume)

    return{
        "distinctOperatorCount": distinctOperatorCount,
        "distinctOperandCount" : distinctOperandCount,
        "totalOperatorCount": totalOperatorCount,
        "totalOperandCount": totalOperandCount,
        "vocab": vocabulary,
        "length": length,
        "eProgLength": estimatedProgramLength,
        "volume": volume,
        "difficulty": difficulty,
        "effort": effort,
        "time": time,
        "bugsEstimate": bugsEstimate}




# Prints all Halstead Metrics
def PrintAllHalsteadMetrics(sourceCodeFilePath):
    metrics = CalculateAllHalsteadMetrics(sourceCodeFilePath)
    # Prints Basic Counts
    print(f"Number of Distinct Operators: {metrics['distinctOperatorCount']}")
    print(f"Number of Distinct Operands: {metrics['distinctOperandCount']}")
    print(f"Total Number of Operators: {metrics['totalOperatorCount']}")
    print(f"Total Number of Operands: {metrics['totalOperandCount']}\n")

    # Prints Halstead Calculation Results
    print(f"Vocabulary: {metrics['vocab']}")
    print(f"Length: {metrics['length']}")
    print(f"Estimated Program Length: {metrics['eProgLength']}")
    print(f"Volume: {metrics['volume']}")
    print(f"Difficulty: {metrics['difficulty']}")
    print(f"Effort: {metrics['effort']}")
    print(f"Time: {metrics['time']}")
    print(f"Estimated Number of bugs: {metrics['bugsEstimate']}")
    return 0