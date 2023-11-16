a = "dsf\"\\\"\\''\'fdf\"d'fds" + 'sdf\'"'
a = "dsf"
b = 'df'
def P1(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    TEST = "________________________"

    a = "dsf\'fdf\"d'fds"

    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)

    return len(stack) == 0