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
        self.inQuoteBlock = False
        self.inString = False
        self.currentString = ""

        self.line = ""
        self.current = 0


    def TokeniseCode(self, file):
        self.file = file
        # Gets each line in the file and stores tokens in a list
        with open(self.file, 'r', encoding="utf8") as file:
            for line in file:
                self.line = r"".join(line) + "     "
                a = self.line

                # Letter
                self.current = 0
                # Loop through each line
                while self.current <= len(self.line) - 3:
                    if not self.inString:
                        # Skip Comment lines
                        if self.skipComment(self.line[self.current]) and not self.inQuoteBlock:
                            self.current = 0
                            break

                        # TODO Work on skipping quotes
                        # Skip block quotes
                        if self.isQuoteBlockChars():
                            self.current += 3
                            if self.inQuoteBlock:
                                self.inQuoteBlock = False
                            else:
                                self.inQuoteBlock = True
                                continue
                        if self.inQuoteBlock:
                            self.current += 1
                            continue



                    # If String
                    self.inStringBlock(self.line[self.current])
                    if self.inString:
                        string = ""
                        self.current += 1
                        while self.inStringBlock(self.line[self.current]):
                            string += self.line[self.current]
                            self.current += 1
                            if self.line[self.current] == '\\':
                                string += self.line[self.current + 1]
                                self.current += 2
                            '''
                            # Break out of self.line but stay in block
                            if self.current >= len(self.line)-2:
                                self.self.currentString += string
                                return
                            '''
                        self.addToken(string)
                        self.current += 1

                    # Skip Null Tokens
                    if self.skipNullTokens():
                        continue
                    # If Letter
                    if self.line[self.current].isalpha() or self.line[self.current] == '_':
                        word = ""
                        while self.line[self.current].isalpha() or self.line[self.current] == '_' or self.line[self.current].isdigit():
                            word += self.line[self.current]
                            self.current += 1

                        if word != "":
                            self.addToken(word)

                    # Skip Null Tokens
                    if self.skipNullTokens():
                        continue

                    # If Operator
                    # Edge case of ! not being an individual operator
                    if self.line[self.current] in self.operatorTable or self.line[self.current] == '!':
                        operator = ""
                        while self.line[self.current] in self.operatorTable or self.line[self.current] == '!':
                            operator += self.line[self.current]
                            self.current += 1
                        if operator != "":
                            self.addTokenOperator(operator)

                    # Skip Null Tokens
                    if self.skipNullTokens():
                        continue

                    # Digit/number
                    number = ""
                    if self.line[self.current].isdigit():
                        while self.line[self.current].isdigit():
                            number += self.line[self.current]
                            self.current += 1
                            if self.line[self.current] == '.':
                                number += self.line[self.current]
                                self.current += 1
                        self.addToken(number)


        return ((self.operatorCount, self.distinctOperators), (self.operandCount, self.distinctOperands))

    def skipComment(self, token : str) -> bool:
        return token == self.commentChar

    def isQuoteBlockChars(self):
        isQuote = self.line[self.current]
        for i in range(1, 3):
            isQuote += self.line[self.current + i]
        a = isQuote in self.blockQuoteCharsThree
        return isQuote in self.blockQuoteCharsThree


    def skipNullTokens(self):
        while self.isNullToken(self.line[self.current]):
            self.current += 1
            if self.current >= len(self.line)-2:
                return True

    def inStringBlock(self, token):
        if token in self.stringChars:
            self.inString = not self.inString
        return self.inString

    def isNullToken(self, token):
        return token in self.nullTolkens

    def addToken(self, token):
        if token in self.operatorTable:
            self.operatorCount += 1
            self.distinctOperators[token] = token
        else:
            self.operandCount += 1
            self.distinctOperands[token] = token

    def addTokenOperator(self, token):
        if token in self.operatorTable:
            self.operatorCount += 1
            self.distinctOperators[token] = token
        else:
            for t in token:
                self.addToken(t)


#lex = Lexer("lexerEG.py")
#lex.TokeniseCode()
#print(lex.distinctOperands)
#print(lex.distinctOperators)