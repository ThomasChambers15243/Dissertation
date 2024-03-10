import math
from Code import Lexer
"""
File for analyzing code and Performing Halstead Calculations

Halstead Calculations

    n1 = the number of distinct operators
    n2 = the number of distinct operands
    N1 = the total number of operators
    N2 = the total number of operands
    
    Program vocabulary: n = n1 + n2
    Program length: N = N1 + N2
    Calculated program length: N'=n1log2(n1)+n2log2(n2)
    volume: V = Nlog2(n)
    difficulty: D = (n1/2) * (N2/n2)
    effort: E= DV
    time = T = E / 18 sec
    Bugs Estimate = B = V / 3000

Operators are all normal operators, keywords and brackets of all kinds ( (), [], {} )
Operands are variables, methods, constants (False, True, strings and other data type values)
"""


class HalsteadMetrics:
    """
    Calculates and stores Halstead metrics
    """

    def __init__(self, source: str):
        lexer = Lexer.Lexer()
        n1, n2, N1, N2 = lexer.tokenize_code(source)
        self.distinct_operators = n1
        self.distinct_operands = n2
        self.distinct_operator_count = len(self.distinct_operators)
        self.distinct_operand_count = len(self.distinct_operands)
        self.total_operator_count = N1
        self.total_operand_count = N2
        self.metrics = {
            "DistinctOperatorCount": 0,
            "DistinctOperandCount": 0,
            "TotalOperatorCount": 0,
            "TotalOperandCount": 0,
            "vocabulary": 0,
            "length": 0,
            "EstProgLength": 0,
            "volume": 0,
            "difficulty": 0,
            "effort": 0,
            "time": 0,
            "BugsEstimate": 0
        }
        # Calculates and stores the Halstead metrics for the given file
        self.set_metrics()

    def set_metrics(self):
        """
        Sets the instances metrics
        :return: None
        """
        self.metrics["DistinctOperatorCount"] = self.distinct_operator_count
        self.metrics["DistinctOperandCount"] = self.distinct_operand_count
        self.metrics["TotalOperatorCount"] = self.total_operator_count
        self.metrics["TotalOperandCount"] = self.total_operand_count
        self.metrics["vocabulary"] = self.vocabulary()
        self.metrics["length"] = self.length()
        self.metrics["EstProgLength"] = self.estimated_program_length()
        self.metrics["volume"] = self.volume()
        self.metrics["difficulty"] = self.difficulty()
        self.metrics["effort"] = self.effort()
        self.metrics["time"] = self.time()
        self.metrics["BugsEstimate"] = self.bugs_estimate()

    def print_stats(self):
        """
        Prints raw operator and operand counts
        :return: None
        """
        print(f"Number of Distinct Operators: {self.distinct_operator_count}\n")
        print(f"Number of Distinct Operands: {self.distinct_operand_count}\n")
        print(f"Total Number of Operators: {self.total_operator_count}\n")
        print(f"Total Number of Operands: {self.total_operand_count}\n")

    def print_all_halstead_metrics(self):
        """
        Prints all Stats - counts and Halstead Metrics
        :return: None
        """
        self.print_stats()

        # Prints Halstead Calculation Results
        print(f"vocabulary: {self.metrics['vocabulary']}")
        print(f"length: {self.metrics['length']}")
        print(f"Estimated Program length: {self.metrics['EstProgLength']}")
        print(f"volume: {self.metrics['volume']}")
        print(f"difficulty: {self.metrics['difficulty']}")
        print(f"effort: {self.metrics['effort']}")
        print(f"time: {self.metrics['time']}")
        print(f"Estimated Number of bugs: {self.metrics['BugsEstimate']}")

    def vocabulary(self) -> int:
        """
        Calculates vocabulary score
        :return: int
        """
        return round(self.distinct_operator_count + self.distinct_operand_count, 2)

    def length(self) -> int:
        """
        Calculates length
        :return: int
        """
        return round(self.distinct_operator_count + self.distinct_operand_count, 2)

    def estimated_program_length(self) -> float:
        """
        Calculates estimated program length
        :return: float
        """
        try:
            lhs = self.distinct_operator_count * math.log2(float(self.distinct_operator_count))
            rhs = self.distinct_operand_count * math.log2(float(self.distinct_operand_count))
        except ValueError:
            return 0
        return round(lhs + rhs, 2)

    def volume(self) -> float:
        """
        Calculates volume score
        :return: float
        """
        try:
            return round(self.length() * math.log2(float(self.vocabulary())), 2)
        except ValueError:
            return 0

    def difficulty(self) -> float:
        """
        Calculates difficulty score
        :return: float
        """
        try:
            # Catch divide by 0 error
            if self.distinct_operand_count == 0:
                return 0
            else:
                return round((self.distinct_operator_count / 2) * (self.total_operand_count / self.distinct_operand_count), 2)
        except ValueError:
            return 0

    def effort(self) -> float:
        """
        Calculates effort score
        :return: float
        """
        return round(self.difficulty() * self.volume(), 2)

    def time(self) -> float:
        """
        Calculate time to programn score
        :return: float
        """
        return round(self.effort() / 18, 2)

    def bugs_estimate(self) -> float:
        """
        Calculate bug estimate
        :return: float
        """
        return round(self.volume() / 3000, 2)
