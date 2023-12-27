def P2(brackets):
    stack = []
    closing = {'(':')', '[':']', '{':'}'}
    for char in brackets:
        if char in closing.values():
            if len(stack) == 0 or stack.pop() != char:
                return False
        elif char in closing.keys():
            stack.append( closing[char] )
    return len(stack) == 0