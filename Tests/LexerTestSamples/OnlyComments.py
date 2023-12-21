# File testing that comments are excluded from the lexer
# They should not be counted as operators or operands
# All counts should be zero
#
####
# # #
# True
# stringVar = "this is a string"
'''
This is a comment
This is a comment
This is a comment
'''
"""
This is a comment
This is a comment
This is a comment
"""