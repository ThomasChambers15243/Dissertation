'''
Given a string of unknown length, calculate the sum total ASCII value
of all characters, ignoring spaces. Return an integer. 

e.g. “Python” = 642
'''

#TODO
def Q1(s : str) -> int:
    return sum(ord(char) for char in s if char != " ")