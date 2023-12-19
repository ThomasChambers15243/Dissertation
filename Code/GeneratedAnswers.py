def P1(celsius):
    kelvin = round(celsius + 273.15, 2)
    fahrenheit = round((celsius * 9/5) + 32, 2)
    return [kelvin, fahrenheit]

# At T = 0.6
def P2(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack


def P3(string):
    max_length = 0
    current_length = 0
    previous_char = None

    for char in string:
        if char == previous_char:
            current_length += 1
        else:
            current_length = 1
        previous_char = char
        max_length = max(max_length, current_length)

    return max_length

def P4(arr):
    unique_elements = []
    for element in arr:
        if element not in unique_elements:
            unique_elements.append(element)
    return len(unique_elements)

def P5(arr):
    return sorted(arr)