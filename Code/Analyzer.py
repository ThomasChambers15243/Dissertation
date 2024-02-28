import math
from Code import Lexer
from Code import functionality
'''
File for analyzing code and Performing Halstead Calculations

Halstead Calculations

    n1 = the number of distinct operators
    n2 = the number of distinct operands
    N1 = the total number of operators
    N2 = the total number of operands
    
    Program vocabulary: n = n1 + n2
    Program length: N = N1 + N2
    Calculated program length: N'=n1log2(n1)+n2log2(n2)
    Volume: V = Nlog2(n)
    Difficulty: D = (n1/2) * (N2/n2)
    Effort: E= DV
    Time = T = E / 18 sec
    Bugs Estimate = B = V / 3000

Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
Operands are variables, methods, constants (False, True, strings and other data type values)
'''


class HalsteadMetrics:
    """
    Calculates and stores Halstead metrics
    """

    def __init__(self, source: str):
        # Only applies calculations to valid python file
        self.Metrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 0,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 0,
            "Vocabulary": 0,
            "Length": 0,
            "EstProgLength": 0,
            "Volume": 0,
            "Difficulty": 0,
            "Effort": 0,
            "Time": 0,
            "BugsEstimate": 0
        }
        if not functionality.validFile(source):
            return
        lexer = Lexer.Lexer()
        n1, n2, N1, N2 = lexer.TokenizeCode(source)
        self.distinctOperators = n1
        self.distinctOperands = n2
        self.distinctOperatorCount = len(self.distinctOperators)
        self.distinctOperandCount = len(self.distinctOperands)
        self.totalOperatorCount = N1
        self.totalOperandCount = N2

        # Calculates and stores the Halstead metrics for the given file
        self.SetMetrics()

    def SetMetrics(self):
        """
        Sets the instances metrics
        :return: None
        """
        self.Metrics["DistinctOperatorCount"] = self.distinctOperatorCount
        self.Metrics["DistinctOperandCount"] = self.distinctOperandCount
        self.Metrics["TotalOperatorCount"] = self.totalOperatorCount
        self.Metrics["TotalOperandCount"] = self.totalOperandCount
        self.Metrics["Vocabulary"] = self.Vocabulary()
        self.Metrics["Length"] = self.Length()
        self.Metrics["EstProgLength"] = self.EstimatedProgramLength()
        self.Metrics["Volume"] = self.Volume()
        self.Metrics["Difficulty"] = self.Difficulty()
        self.Metrics["Effort"] = self.Effort()
        self.Metrics["Time"] = self.Time()
        self.Metrics["BugsEstimate"] = self.BugsEstimate()

    def PrintStats(self):
        """
        Prints raw operator and operand counts
        :return: None
        """
        print(f"Number of Distinct Operators: {self.distinctOperatorCount}\n")
        print(f"Number of Distinct Operands: {self.distinctOperandCount}\n")
        print(f"Total Number of Operators: {self.totalOperatorCount}\n")
        print(f"Total Number of Operands: {self.totalOperandCount}\n")

    def PrintAllHalsteadMetrics(self):
        """
        Prints all Stats - counts and Halstead Metrics
        :return: None
        """
        self.PrintStats()

        # Prints Halstead Calculation Results
        print(f"Vocabulary: {self.Metrics['Vocabulary']}")
        print(f"Length: {self.Metrics['Length']}")
        print(f"Estimated Program Length: {self.Metrics['EstProgLength']}")
        print(f"Volume: {self.Metrics['Volume']}")
        print(f"Difficulty: {self.Metrics['Difficulty']}")
        print(f"Effort: {self.Metrics['Effort']}")
        print(f"Time: {self.Metrics['Time']}")
        print(f"Estimated Number of bugs: {self.Metrics['BugsEstimate']}")

    def Vocabulary(self) -> int:
        """
        Calculates vocabulary score
        :return: int
        """
        return self.distinctOperatorCount + self.distinctOperandCount

    def Length(self) -> int:
        """
        Calculates length
        :return: int
        """
        return self.distinctOperatorCount + self.distinctOperandCount

    def EstimatedProgramLength(self) -> float:
        """
        Calculates estimated program length
        :return: float
        """
        try:
            lhs = self.distinctOperatorCount * math.log2(float(self.distinctOperatorCount))
            rhs = self.distinctOperandCount * math.log2(float(self.distinctOperandCount))
        except ValueError:
            return 0
        return lhs + rhs

    def Volume(self) -> float:
        """
        Calculates volume score
        :return: float
        """
        try:
            return self.Length() * math.log2(float(self.Vocabulary()))
        except ValueError:
            return 0

    def Difficulty(self) -> float:
        """
        Calculates difficulty score
        :return: float
        """
        try:
            # Catch divide by 0 error
            if self.distinctOperandCount == 0:
                return 0
            else:
                return (self.distinctOperatorCount / 2) * (self.totalOperandCount / self.distinctOperandCount)
        except ValueError:
            return 0

    def Effort(self) -> float:
        """
        Calculates Effort score
        :return: float
        """
        return self.Difficulty() * self.Volume()

    def Time(self) -> float:
        """
        Calculate time to programn score
        :return: float
        """
        return self.Effort() / 18

    def BugsEstimate(self) -> float:
        """
        Calculate bug estimate
        :return: float
        """
        return self.Volume() / 3000
