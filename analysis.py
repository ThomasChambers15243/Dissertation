import math


class Analyser:
    def __init__(self, SourceCodeFilePath):
        self.SourceCodeFilePath = SourceCodeFilePath
        self.tokenCounts = {
            "operatorCount" : 0,
            "operandCount" : 0,
            "distinctOperators" : {},
            "distinctOperands" : {}}
        self.rawLine = r""
        self.currentIndex = 0
        # Hash Map of all operator Tokens in Python
        self.OP_TABLE = {
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

        self.Tokenise()

    ### Counts the number of operators and operands in the file
    def Tokenise(self):
        with open(self.SourceCodeFilePath, "r") as file:
            for line in file:
                # Gets each line in the file as a raw string to avoid any special characters
                self.rawLine = r"".join(line) + "   "
                while self.currentIndex < len(self.rawLine):
                    token = self.rawLine[self.currentIndex]
                    if self._ShouldAvoidToken(token) : continue
                    # Analyse token
                    if self._CountWord(token) : continue
                    if self._CountNumber(token) : continue
                    if self._CountString(token) : continue
                    if self._CountSingleOperators(token) : continue
        return


    def _ShouldAvoidToken(self, token):
        if (
            self._NullToken(token)
            or self._CommentToken(token)
            or self._TrippleCommentToken(token)
        ):
            return True
        return False

    # Avoids null characters
    def _NullToken(self, token):
        if token in [' ', '\n', ',']:
            self.currentIndex += 1
            return True
        return False

    # Avoids Comments
    def _CommentToken(self, token):
        if token == "#":
            self.currentIndex = len(self.rawLine)
            return True
        return False

    # Avoids Comments
    def _TrippleCommentToken(self, token):
        if token in ["'", '"', '`']:
            quote = self.rawLine[self.currentIndex] + \
                    self.rawLine[self.currentIndex + 1] + \
                    self.rawLine[self.currentIndex + 2]
            if quote in [r"'''", r'"""', r"```"]:
                self.currentIndex += 3
            return True
        return False

    # Counts Words
    def _CountWord(self, token):
        if (
            not token.isalpha()
            and token != "_"
            and token + self.rawLine[self.currentIndex + 1] != "__"
        ):
            return False
        word = ""
        # Loops until the end of the word
        while self.rawLine[self.currentIndex].isalpha() or self.rawLine[self.currentIndex] == "_" or self.rawLine[self.currentIndex].isdigit():
            word += self.rawLine[self.currentIndex]
            self.currentIndex += 1
        # Updates token counts
        if word in self.OP_TABLE:
            self.tokenCounts["operatorCount"] += 1
            self.currentIndex += 1
            if word not in self.tokenCounts["distinctOperators"]:
                self.tokenCounts["distinctOperators"][word] = self.OP_TABLE[word]
        else:
            self.tokenCounts["operandCount"] += 1
            if word not in self.tokenCounts["distinctOperands"]:
                self.tokenCounts["distinctOperands"][word] = word
        return True

    # Counts Numbers
    def _CountNumber(self, token):
        if self._ShouldAvoidToken(token):
            return False
        if token.isdigit():
            number = ""
            # Loops until end of the number
            while self.rawLine[self.currentIndex].isdigit():
                number += self.rawLine[self.currentIndex]
                self.currentIndex += 1
            # Updates token counts
            if number not in self.tokenCounts["distinctOperands"]:
                self.tokenCounts["distinctOperands"][number] = number
            self.tokenCounts["operandCount"] += 1
            return True

    # Counts strings
    def _CountString(self, token):
        if token not in ["'", '"'] or self._ShouldAvoidToken(token):
            return False
        stringValue = ""
        self.currentIndex += 1
        # Loops until the end of string character, either " or '
        while self.rawLine[self.currentIndex] != token:
            stringValue += self.rawLine[self.currentIndex]
            self.currentIndex += 1
            if self.rawLine[self.currentIndex] == r'\\':
                self.currentIndex += 2
        # updates token counts
        if stringValue not in self.tokenCounts["distinctOperands"]:
            self.tokenCounts["distinctOperands"][stringValue] = stringValue
        self.tokenCounts["operandCount"] += 1
        self.tokenCounts["currentIndex"] += 1
        return True

    # Counts single operators
    def _CountSingleOperators(self, token):
        if self._ShouldAvoidToken(token):
            return False
        if token in self.OP_TABLE:
            self.currentIndex += 1
            if token not in self.tokenCounts["distinctOperators"]:
                self.tokenCounts["distinctOperators"][token] = self.OP_TABLE[token]
        else:
            value = ""
            while value not in self.OP_TABLE:
                value += self.rawLine[self.currentIndex]
                self.currentIndex += 1
            if value not in self.tokenCounts["distinctOperators"]:
                self.tokenCounts["distinctOperators"][value] = value
        self.tokenCounts["operatorCount"] += 1
        return True
