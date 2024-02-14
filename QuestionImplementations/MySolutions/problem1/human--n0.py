'''
You are given a list of tuples containing two integers represented as strings, of n length.
Each tuple represents a floating point number, the first string is the integer and the second is the decimal.
Find the total of all floating point numbers in the list.
Return a float

e.g. [ ('1','0'), ('32','15') ] = 1.0 + 32.15 = 33.15
'''

#TODO
def Q2(floatList) -> float:
    return sum(float(f"{i}.{j}") for i, j in floatList)