# New Lexer

__OP_TABLE = {
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

class Lexer:
    def __init__(self, sourceFile):
        self.operatorCount = 0;
        self.operandCount = 0;
        self.distinctOperators = {}
        self.distinctOperands = {}
        self.file = sourceFile
        self.blockQuoteCharsThree = ["'''", '"""']
        self.blockQuoteCharsSix = ["''''''", '""""""']
        self.commentChar = "#"
        self.inQuoteBlock = False

    def tokenise(self):
        # Gets each line in the file and stores tokens in a list
        with open(self.file,'r',encoding="utf8") as file:
            for line in file:
                line = r"".join(line)
                line = line.split()

                # Calculates what each token is
                for token in line:
                    # Skip Comment lines
                    if self.skipComment(token):
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

                    # If Number

                    # If String

                    # Single Op


                    print(token)

    def skipComment(self, token) -> bool:
        return token == self.commentChar

    def skipBlockQuoteThree(self, token) -> bool:
        return token in self.blockQuoteCharsThree

    def skipBlockQuoteSix(self, token) -> bool:
        return token in self.blockQuoteCharsSix

lex = Lexer("lexerEG.py")
lex.tokenise()