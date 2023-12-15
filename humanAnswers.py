def P1(celsius):
    return [ round(celsius + 273.15, 2), round((celsius * 9/5) + 32, 2) ]

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

def P3(inputs):
    if not inputs:
        return 0

    max_count = -1
    start_idx = 0
    for idx, char in enumerate(inputs,1):
        print( "> ", start_idx, idx, inputs[start_idx], inputs[idx] )
        if inputs[start_idx] != inputs[idx]:
            max_count = max( idx - start_idx, max_count )
            start_idx = idx
    return max_count

def P4(dups):
    return len(set(dups))

def P5(ints):
    return sorted(ints)