import math

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


# Hash Map of all operator Tokens in Python
OP_TABLE = {
    # Assingment
    "+=" : "op",
    "*=" : "op",
    "/=" : "op",
    "%=" : "op",
    "**=" : "op",
    "//=" : "op",
    "=" : "op",
    "." : "op",
    # Arithmetric
    "+" : "op",
    "-" : "op",
    "*" : "op",
    "/" : "op",
    "\\": "op",
    "%" : "op",
    "**" : "op",
    # Comparison
    "==" : "op",
    "!=" : "op",
    ">" : "op",
    "<" : "op",
    ">=" : "op",
    "<=" : "op",
    # Bitwise
    "&" : "op",
    "|" : "op",
    "^" : "op",
    "~" : "op",
    "<<" : "op",
    ">>" : "op",
    # Brackets and New Path
    "(" : "op",
    ")" : "op",
    "{" : "op",
    "}" : "op",
    "[" : "op",
    "]" : "op",
    ":" : "op",
    ";" : "op",
    "@" : "op",
    # Keyword
    "and" : "op",
    "or" : "op",
    "not" : "op",
    "None" : "op",
    "as" : "op",
    "assert" : "op",
    "async" : "op",
    "await" : "op",
    "break" : "op",
    "class" : "op",
    "continue" : "op",
    "def" : "op",
    "del" : "op",
    "elif" : "op",
    "else" : "op",
    "except" : "op",
    "finally" : "op",
    "for" : "op",
    "from" : "op",
    "global" : "op",
    "if" : "op",
    "import" : "op",
    "in" : "op",
    "is" : "op",
    "lambda" : "op",
    "nonlocal" : "op",
    "pass" : "op",
    "raise" : "op",
    "return" : "op",
    "try" : "op",
    "while" : "op",
    "with" : "op",
    "yield" : "op",
}

# Turns the code into useable tokens for Halstead Calculations
# Returns an array of two tuples
# [ (int: Operator Count , dict: Unique Operators) , (int: Operand Count , dict: Unique Operands)
def TokeniseCode(SourceCodeFilePath):
    operatorCount = 0;
    operandCount = 0;

    distinctOperators = {}
    distinctOperands = {}

    nullTolkens = [' ', '\n',',']

    with open(SourceCodeFilePath, "r") as file:
        for sline in file:
            line = r"".join(sline) + "   "
            # Set up token search
            current = 0
            while current < len(line):
                token = line[current]
                if token in nullTolkens:
                    current += 1
                    continue
                # Skip Comments
                if token == "#":
                    current = len(line)
                    continue
                if token in ["'", '"', '`']:
                    quote = line[current] + line[current+1] + line[current+2]
                    if quote in [r"'''", r'"""', r"```"]:
                        current += 3
                        continue

                # Letter
                if token.isalpha() or token == "_" or ((token + line[current+1]) == "__"):
                    word = ""
                    while line[current].isalpha() or line[current] == "_" or line[current].isdigit():
                        word += line[current]
                        current += 1
                    if word in OP_TABLE:
                        if word not in distinctOperators:
                            distinctOperators[word] = OP_TABLE[word]
                        operatorCount += 1
                        current += 1
                    else:
                        operandCount += 1
                        if word not in distinctOperands:
                            distinctOperands[word] = word
                    continue

                # Number
                if token.isdigit():
                    number = ""
                    while line[current].isdigit():
                        number += line[current]
                        current += 1
                    if number not in distinctOperands:
                        distinctOperands[number] = number
                    operandCount += 1
                    continue

                # String
                if token in ['"', "'"]:
                    stringValue = ""
                    current += 1
                    while line[current] != token:
                        stringValue += line[current]
                        current += 1
                        if line[current] == r'\\':
                            current += 2
                    if stringValue not in distinctOperands:
                        distinctOperands[stringValue] = stringValue
                    operandCount += 1
                    current += 1
                    continue

                # Single Ops
                if token in OP_TABLE:
                    if token not in distinctOperators:
                        distinctOperators[token] = OP_TABLE[token]
                    current += 1
                else:
                    value = ""
                    while value not in OP_TABLE:
                        value += line[current]
                        current += 1
                    if value not in distinctOperators:
                        distinctOperators[value] = value
                operatorCount += 1
    return [(operatorCount,distinctOperators), (operandCount, distinctOperands)]

# DistinctOperatorCount,distinctOperandCount,totalOperatorCount,totalOperandCount
# n1                    n2                 N1                   N2
def ShowOperatorAndOperandStats(sourceCodeFilePath):
    # Tokenize the code and get the metrics
    operators, operands = TokeniseCode(sourceCodeFilePath)

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
    lhs = distinctOperatorCount * math.log2(distinctOperatorCount)
    rhs = distinctOperandCount * math.log2(distinctOperandCount)
    return lhs + rhs

def Volume(totalOperatorCount, totalOperandCount, distinctOperatorCount, distinctOperandCount):
    return Length(totalOperatorCount, totalOperandCount) * math.log2(
        Vocabulary(distinctOperatorCount, distinctOperandCount)
    )

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
    operators, operands = TokeniseCode(sourceCodeFilePath)

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