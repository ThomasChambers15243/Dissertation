import os
import openai

class Generation:
    def __innit__(self):
        # Class constructor
        self.openai.api_key = os.environ['API_KEY']
        self.MODEL = "gpt-3.5-turbo"

    # Gets response from openAI,
    # returns it as a string
    def GetResponce(self, content, temperature=0.6):

        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {
                "role": "user", "content": content },
                {"role": "user", "content": "Any code you are asked to write, return only the code. No explenation or tests of the code. No extra notes. All of the responce should be able to immediately run. The first line of code should be the first function in the programn. No comments or explenations of the code"}
            ],
            temperature=temperature,
        )

        return response['choices'][0]['message']['content']