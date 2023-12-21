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

def SkipNullTokens(token, current) -> (bool,int):
    nullTolkens = [' ', '\n', ',']
    if token in nullTolkens:
        current += 1
        return True, current
    return False, current

def SkipSingleComments(token, current, line) -> (bool, int):
    # Skip Hash Comments
    if token == "#":
        return True, len(line)
    return False, current

def isBlockQuote(token, current, line) -> bool:
    isQuote = token + line[current + 1] + line[current + 2]
    if isQuote == token * 3:
        return True
    return False

'''
Turns the code into useable tokens for Halstead Calculations
Returns an tuple of two tuples
( (int: Operator Count , dict: Unique Operators) , (int: Operand Count , dict: Unique Operands) )
'''
def TokeniseCode(SourceCodeFilePath):
    operatorCount = 0;
    operandCount = 0;

    distinctOperators = {}
    distinctOperands = {}

    with open(SourceCodeFilePath, "r") as file:
        inQuoteBlock = False
        blockQuoteChars = ["'", '"', '`', '\"', "\'", "\`"]
        for sline in file:
            line = r"".join(sline) + "   "
            # Set up token search
            current = 0

            while current < len(line):
                # Skip Code Block
                if line[current] in blockQuoteChars or inQuoteBlock:
                    blockQuote = isBlockQuote(line[current], current, line)
                    if inQuoteBlock:
                        current = len(line)
                        if blockQuote:
                            inQuoteBlock = False
                        continue
                    else:
                        current = len(line)
                        if blockQuote:
                            inQuoteBlock = True
                        continue

                # Skip null Tokens
                valid, current = SkipNullTokens(line[current], current)
                if valid:
                    continue;

                # Skip Single Comments
                valid, current = SkipSingleComments(line[current], current, line)
                if valid:
                    continue;

                # Letter
                # Abstract away, return word and use len(word) to calculate how much to
                # increment current by
                if line[current].isalpha() or line[current] == "_" or ((line[current] + line[current+1]) == "__"):
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
                if line[current].isdigit():
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
                if line[current] in ['"', "'"]:
                    stringValue = ""
                    current += 1
                    while line[current] != line[current]:
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
                if line[current] in OP_TABLE:
                    if line[current] not in distinctOperators:
                        distinctOperators[line[current]] = OP_TABLE[line[current]]
                    current += 1
                else:
                    value = ""
                    while value not in OP_TABLE:
                        value += line[current]
                        current += 1
                    if value not in distinctOperators:
                        distinctOperators[value] = value
                operatorCount += 1
    return ((operatorCount,distinctOperators), (operandCount, distinctOperands))
