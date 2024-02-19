import random

# Example Script

def GetRandomNumber(lower, upper):
    return random.randint(lower, upper)

if GetRandomNumber(0, 100) > 50:
    print("Small")
else:
    print("Large")
