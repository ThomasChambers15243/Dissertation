import Generation
import Analyzer

#p1 = Generation.GetResponce("Given a string s containing just the characters '(', ')', '{', '}', ' [' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order. Every close bracket has a corresponding open bracket of the same type. Name the function P1")
#p2 = Generation.GetResponce("You are given a non-negative floating-point number rounded to two decimal places celsius, that denotes the temperature in Celsius. You should convert Celsius into Kelvin and Fahrenheit and return it as an array ans = [kelvin, fahrenheit]. Name the function P2")
p6 = Generation.GetResponce("Given two arrays of strings, combine them into one sorted array, with the shortest length string at index 0 and the longest length string at the last index. If two strings are the same length, sum up each string’s characters’ ASCII value, and use that total, inserting the smallest first. Return the new array. Name the function P6.")
#print(P6(["a", "cc", "aaaaaa"],["bb","bbb"]))

with open("TestFile.py", "w") as file:
   file.write(p6)
   file.write('\n\n')
   file.write(p6)
Analyzer.CalculateAllHalsteadMetrics("TestFile.py")