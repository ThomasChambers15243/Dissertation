class Lexer:
    """
    Tokenizes a python file into operators and operands
    Suitable for use in Halstead Complexity Measures
    """

    def __init__(self):
        # Returned Counts
        self.operatorCount = 0;
        self.operandCount = 0;
        self.distinctOperators = {}
        self.distinctOperands = {}
        # Valid Operators
        self.operatorTable = {
            # Assingment
            "+=": "op",
            "*=": "op",
            "/=": "op",
            "%=": "op",
            "**=": "op",
            "//=": "op",
            "=": "op",
            ".": "op",
            # Arithmetric
            "+": "op",
            "-": "op",
            "*": "op",
            "/": "op",
            "\\": "op",
            "%": "op",
            "**": "op",
            # Comparison
            "==": "op",
            "!=": "op",
            ">": "op",
            "<": "op",
            ">=": "op",
            "<=": "op",
            # Bitwise
            "&": "op",
            "|": "op",
            "^": "op",
            "~": "op",
            "<<": "op",
            ">>": "op",
            # Brackets and New Path
            "(": "op",
            ")": "op",
            "{": "op",
            "}": "op",
            "[": "op",
            "]": "op",
            ":": "op",
            ";": "op",
            "@": "op",
            "->": "op",
            # Keyword
            "and": "op",
            "or": "op",
            "not": "op",
            "None": "op",
            "as": "op",
            "assert": "op",
            "async": "op",
            "await": "op",
            "break": "op",
            "class": "op",
            "continue": "op",
            "def": "op",
            "del": "op",
            "elif": "op",
            "else": "op",
            "except": "op",
            "finally": "op",
            "for": "op",
            "from": "op",
            "global": "op",
            "if": "op",
            "import": "op",
            "in": "op",
            "is": "op",
            "lambda": "op",
            "nonlocal": "op",
            "pass": "op",
            "raise": "op",
            "return": "op",
            "try": "op",
            "while": "op",
            "with": "op",
            "yield": "op",
        }
        # File Path
        self.file = None
        # Char Types
        self.blockQuoteCharsThree = ["'''", '"""']
        self.commentChar = "#"
        self.nullTolkens = [' ', '\n', ',']
        self.stringChars = ["'", '"']
        # Flags
        self.inQuoteBlock = False
        self.inString = False
        # Line Trackers
        self.currentString = ""
        self.line = ""
        self.current = 0

    def TokenizeCode(self, file: str) -> tuple:
        """
        Tokenises the code in the file as compatible Halstead operands and operators
        :param file: File Path
        :return: operator and operand counts and distinct operators and operands dictionary
        """
        # Gets each line in the file and stores tokens in a list
        self.file = file
        with open(self.file, 'r', encoding="utf8") as file:
            for line in file:
                # Adds 5 spaces to the end of the line to prevent index out of range errors
                self.line = r"".join(line) + "     "
                self.current = 0
                # Loop through each line
                while self.current <= len(self.line) - 3:
                    # Handles comments and Blocks
                    if not self.inString:
                        if self.handleComments():
                            break
                        if self.isQuoteBlockChars() and self.handleBlockQuote():
                            continue
                        if self.inQuoteBlock:
                            self.current += 1
                            continue

                    # Checks String
                    if self.inStringBlock():
                        self.addString()

                    # Skip Null Tokens
                    if self.skipNullTokens():
                        continue

                    # Checks Letter
                    if self.line[self.current].isalpha() or self.line[self.current] == '_':
                        self.addOperand()

                    # Checks Operator
                    if self.isOperatorChar():
                        self.addOperator()

                    # Digit/number
                    if self.line[self.current].isdigit():
                        self.addNumber()

        return self.operatorCount, self.distinctOperators, self.operandCount, self.distinctOperands

    def handleComments(self) -> bool:
        """
        Resets the current index to 0 if the current line is a comment
        :return: Bool
        """
        if self.line[self.current] == self.commentChar and not self.inQuoteBlock:
            self.current = 0
            return True
        return False

    def handleBlockQuote(self) -> bool:
        """
        Skips block quote chars and flips inQuoteBlock flag
        :return: Bool
        """
        self.current += 3
        self.inQuoteBlock = not self.inQuoteBlock
        return self.inQuoteBlock

    def isQuoteBlockChars(self) -> bool:
        """
        Uses a lookahead to check if the current token is a block quote
        :return: bool
        """
        isQuote = self.line[self.current]
        for i in range(1, 3):
            isQuote += self.line[self.current + i]
        return isQuote in self.blockQuoteCharsThree

    def skipNullTokens(self) -> bool:
        """
        Skips null tokens
        :return: bool
        """
        while self.isNullToken():
            self.current += 1
            if self.current >= len(self.line) - 2:
                return True
        return False

    def inStringBlock(self) -> bool:
        """
        Flips inString flag if token is a string character
        :return: bool
        """
        if self.line[self.current] in self.stringChars:
            self.inString = not self.inString
        return self.inString

    def addString(self) -> None:
        """
        Gets string and adds it to the token list
        :return: None
        """
        string = ""
        self.current += 1
        # Loops until end of string character is found. Does not add "|' to string
        while self.inStringBlock():
            string += self.line[self.current]
            self.current += 1
            # Handles escape characters
            if self.line[self.current] == '\\':
                string += self.line[self.current + 1]
                self.current += 2
        # Adds token and updates current to skip " character
        self.addToken(string)
        self.current += 1

    def addOperand(self) -> None:
        """
        Gets Operand and adds it to the token list
        :return: None
        """
        word = ""
        while self.isWordChar():
            word += self.line[self.current]
            self.current += 1
        if word != "":
            self.addToken(word)

    def addOperator(self) -> None:
        """
        Gets Operator and adds it to the token list
        :return: None
        """
        operator = ""
        while self.isOperatorChar():
            operator += self.line[self.current]
            self.current += 1
        if operator != "":
            self.addTokenOperator(operator)

    def addNumber(self) -> bool:
        """
        Gets Number and adds it to the token list
        :return: None
        """
        number = ""
        while self.line[self.current].isdigit():
            number += self.line[self.current]
            self.current += 1
            # Accounts for floats
            if self.line[self.current] == '.':
                number += self.line[self.current]
                self.current += 1
        if number != "":
            self.addToken(number)

    def isNullToken(self) -> bool:
        """
        Checks if token is a null token
        :return: bool
        """
        return self.line[self.current] in self.nullTolkens

    def isWordChar(self) -> bool:
        """
        Checks if token is a word character
        :return: bool
        """
        return self.line[self.current].isalpha() or self.line[self.current] == '_' or self.line[self.current].isdigit()

    def isOperatorChar(self) -> bool:
        """
        Checks if token is an operator character
        :return: bool
        """
        return self.line[self.current] in self.operatorTable or self.line[self.current] == '!'

    def addToken(self, token : str) -> None:
        """
        Adds token to the distinctOperators or distinctOperands dictionary
        :param token: Token to be added
        :return: None
        """
        if token in self.operatorTable:
            self.operatorCount += 1
            self.distinctOperators[token] = token
        else:
            self.operandCount += 1
            self.distinctOperands[token] = token

    def addTokenOperator(self, token : str) -> bool:
        """
        Added operators to token list. Accounts for strings of operators.
        :param token: Token to be added
        :return: None
        """
        if token in self.operatorTable:
            self.operatorCount += 1
            self.distinctOperators[token] = token
        else:
            for t in token:
                self.addToken(t)
