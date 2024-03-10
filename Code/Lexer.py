class Lexer:
    """
    Tokenizes a python file into operators and operands
    Suitable for use in Halstead Complexity Measures
    """

    def __init__(self):
        # Returned Counts
        self.operator_count = 0;
        self.operand_count = 0;
        self.distinct_operators = {}
        self.distinct_operands = {}
        # Valid Operators
        self.operator_table = {
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
        self.block_quote_chars_three = ["'''", '"""']
        self.comment_char = "#"
        self.null_tolkens = [' ', '\n', ',']
        self.string_chars = ["'", '"']
        # Flags
        self.in_quote_block = False
        self.in_string = False
        # Line Trackers
        self.current_string = ""
        self.line = ""
        self.current = 0

    def tokenize_code(self, file: str) -> tuple:
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
                    if not self.in_string:
                        if self.handle_comments():
                            break
                        if self.is_quote_block_chars() and self.handle_block_quote():
                            continue
                        if self.in_quote_block:
                            self.current += 1
                            continue

                    # Checks String
                    if self.in_string_block():
                        self.add_string()

                    # Skip Null Tokens
                    if self.skip_null_tokens():
                        continue

                    # Checks Letter
                    if self.line[self.current].isalpha() or self.line[self.current] == '_':
                        self.add_operand()

                    # Checks Operator
                    if self.is_operator_char():
                        self.add_operator()

                    # Digit/number
                    if self.line[self.current].isdigit():
                        self.add_number()

        return self.distinct_operators, self.distinct_operands, self.operator_count, self.operand_count

    def handle_comments(self) -> bool:
        """
        Resets the current index to 0 if the current line is a comment
        :return: Bool
        """
        if self.line[self.current] == self.comment_char and not self.in_quote_block:
            self.current = 0
            return True
        return False

    def handle_block_quote(self) -> bool:
        """
        Skips block quote chars and flips inQuoteBlock flag
        :return: Bool
        """
        self.current += 3
        self.in_quote_block = not self.in_quote_block
        return self.in_quote_block

    def is_quote_block_chars(self) -> bool:
        """
        Uses a lookahead to check if the current token is a block quote
        :return: bool
        """
        is_quote = self.line[self.current]
        for i in range(1, 3):
            is_quote += self.line[self.current + i]
        return is_quote in self.block_quote_chars_three

    def skip_null_tokens(self) -> bool:
        """
        Skips null tokens
        :return: bool
        """
        while self.is_null_token():
            self.current += 1
            if self.current >= len(self.line) - 2:
                return True
        return False

    def in_string_block(self) -> bool:
        """
        Flips inString flag if token is a string character
        :return: bool
        """
        if self.line[self.current] in self.string_chars:
            self.in_string = not self.in_string
        return self.in_string

    def add_string(self) -> None:
        """
        Gets string and adds it to the token list
        :return: None
        """
        string = ""
        self.current += 1
        # Loops until end of string character is found. Does not add "|' to string
        while self.in_string_block():
            string += self.line[self.current]
            self.current += 1
            # Handles escape characters
            if self.line[self.current] == '\\':
                string += self.line[self.current + 1]
                self.current += 2
        # Adds token and updates current to skip " character
        self.add_token(string)
        self.current += 1

    def add_operand(self) -> None:
        """
        Gets Operand and adds it to the token list
        :return: None
        """
        word = ""
        while self.is_word_char():
            word += self.line[self.current]
            self.current += 1
        if word != "":
            self.add_token(word)

    def add_operator(self) -> None:
        """
        Gets Operator and adds it to the token list
        :return: None
        """
        operator = ""
        while self.is_operator_char():
            operator += self.line[self.current]
            self.current += 1
        if operator != "":
            self.add_token_operator(operator)

    def add_number(self) -> bool:
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
            self.add_token(number)

    def is_null_token(self) -> bool:
        """
        Checks if token is a null token
        :return: bool
        """
        return self.line[self.current] in self.null_tolkens

    def is_word_char(self) -> bool:
        """
        Checks if token is a word character
        :return: bool
        """
        return self.line[self.current].isalpha() or self.line[self.current] == '_' or self.line[self.current].isdigit()

    def is_operator_char(self) -> bool:
        """
        Checks if token is an operator character
        :return: bool
        """
        return self.line[self.current] in self.operator_table or self.line[self.current] == '!'

    def add_token(self, token : str) -> None:
        """
        Adds token to the distinctOperators or distinctOperands dictionary
        :param token: Token to be added
        :return: None
        """
        if token in self.operator_table:
            self.operator_count += 1
            self.distinct_operators[token] = token
        else:
            self.operand_count += 1
            self.distinct_operands[token] = token

    def add_token_operator(self, token : str) -> bool:
        """
        Added operators to token list. Accounts for strings of operators.
        :param token: Token to be added
        :return: None
        """
        if token in self.operator_table:
            self.operator_count += 1
            self.distinct_operators[token] = token
        else:
            for t in token:
                self.add_token(t)
