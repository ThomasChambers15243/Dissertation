import Generation
import Analyzer

# p1 = Generation.GetResponce("Given a string s containing just the characters '(', ')', '{', '}', ' [' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order. Every close bracket has a corresponding open bracket of the same type. Name the function P1")
# p2 = Generation.GetResponce("You are given a non-negative floating-point number rounded to two decimal places celsius, that denotes the temperature in Celsius. You should convert Celsius into Kelvin and Fahrenheit and return it as an array ans = [kelvin, fahrenheit]. Name the function P2")

# with open("TestFile.py", "w") as file:
#     file.writelines(p1)

Analyzer.CalculateAllHalsteadMetrics("TestFile.py")