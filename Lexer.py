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
                        if line[current] == '.':
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