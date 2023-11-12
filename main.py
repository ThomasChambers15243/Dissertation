import os
import openai

openai.api_key = os.environ['API_KEY']

MODEL = "gpt-3.5-turbo"

response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {
        "role": "user", "content": "Given a string s containing just the characters '(', ')', '{', '}', ' [' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order. Every close bracket has a corresponding open bracket of the same type. Name the function TEST1" },
        {"role": "user", "content": "Any code you are asked to write, return only the code. No explenation or tests of the code. No extra notes. The first line of code should be the first function in the programn"}
    ],
    temperature=0,
)
code = response['choices'][0]['message']['content']

print(code)