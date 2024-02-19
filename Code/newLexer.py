# New Lexer

import os



class Lexer:
    def __init__(self):
        self.operatorCount = 0;
        self.operandCount = 0;
        self.distinctOperators = {}
        self.distinctOperands = {}
        self.file = None
        self.blockQuoteCharsThree = ["'''", '"""']
        self.blockQuoteCharsSix = ["''''''", '""""""']
        self.commentChar = "#"
        self.stringChars = ["'", '"']
        self.nullTolkens = [' ', '\n', ',']
        self.inQuoteBlock = False
        self.inString = False
        self.currentString = ""
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
            "->" : "op",
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
        # get the current working directory
        print(os.getcwd())

    def TokeniseCode(self, file):
        self.file = file
        # Gets each line in the file and stores tokens in a list
        with open(self.file, 'r', encoding="utf8") as file:
            for line in file:
                line = r"".join(line)
                line = line.split()

                # Calculates what each token is
                for token in line:
                    if not self.inString:
                        # Skip Comment lines
                        if self.skipComment(token[0]):
                            break
                        # Skip block quotes
                        if self.skipBlockQuoteThree(token):
                            self.inQuoteBlock = not self.inQuoteBlock
                            continue
                        if self.skipBlockQuoteSix(token):
                            continue
                        if self.inQuoteBlock:
                            continue

                    # Letter
                    if self.lexLine(line):
                        break
                    # If Number

                    # If String

                    # Single Op

        return ((self.operatorCount, self.distinctOperators), (self.operandCount, self.distinctOperands))

    def skipComment(self, token : str) -> bool:
        return token == self.commentChar

    def skipBlockQuoteThree(self, token : str) -> bool:
        return token in self.blockQuoteCharsThree

    def skipBlockQuoteSix(self, token : str) -> bool:
        return token in self.blockQuoteCharsSix

    def lexLine(self, line : list[str]):
        line = " ".join(line) + "   "
        current = 0
        while current < len(line) - 3:
            # If String
            self.inStringBlock(line[current])
            if self.inString:
                string = ""
                current += 1
                while self.inStringBlock(line[current]):
                    string += line[current]
                    current += 1
                    if line[current] == '\\':
                        current += 2
                    '''
                    # Break out of line but stay in block
                    if current >= len(line)-2:
                        self.currentString += string
                        return
                    '''
                self.addToken(string)
                current += 1

            # Skip Null Tokens
            while self.skipNullTokens(line[current]):
                if current >= len(line) - 3:
                    return
                current += 1

            # If Letter
            if line[current].isalpha() or line[current] == '_':
                word = ""
                while line[current].isalpha() or line[current] == '_' or line[current].isdigit():
                    word += line[current]
                    current += 1
                # Hacky but works for now.
                if line[current-1].isalpha() or line[current] == '_' or line[current].isdigit():
                    current -= 1
                if word != "":
                    self.addToken(word)
            else:
                # If Operator
                operator = ""
                a = line[current]
                # Edge case of ! not being an individual operator
                while line[current] in self.operatorTable or line[current] == '!':
                    operator += line[current]
                    current += 1
                if line[current] not in self.operatorTable:
                    current -= 1
                self.addToken(operator)
            current += 1
        return True

    def inStringBlock(self, token):
        if token in self.stringChars:
            self.inString = not self.inString
        return self.inString

    def skipNullTokens(self, token):
        return token in self.nullTolkens

    def addToken(self, token):
        if token in self.operatorTable:
            self.operatorCount += 1
            self.distinctOperators[token] = token
        else:
            self.operandCount += 1
            self.distinctOperands[token] = token


#lex = Lexer("lexerEG.py")
#lex.TokeniseCode()
#print(lex.distinctOperands)
#print(lex.distinctOperators)