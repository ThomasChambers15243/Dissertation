import openai
from config import API_KEY

# Innits the Key
openai.api_key = API_KEY

# Engines Model
MODEL = "gpt-3.5-turbo"


def GetResponce(prompt: str, temperature=0.6) -> str:
    """
    Gets a responce from the GPT-3.5 API
    :param prompt: Prompt to pass through
    :param temperature: Desired temperature of model
    :return: String of responce
    """
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
            "role": "user", "content": prompt },
            {"role": "user", "content": """Any code you are asked to write, return only the code. No explanation or
                                        tests of the code. No extra notes. All of the responses should be able to
                                        immediately run. The first line of code should be the first function in the
                                        program. No comments or explanations of the code. 
                                        Include any code as provided in the prompt without changes to that code"""}
        ],
        temperature=temperature,
    )
    return response['choices'][0]['message']['content']
