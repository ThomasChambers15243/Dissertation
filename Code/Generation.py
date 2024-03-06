import openai
import sys
from loguru import logger
from config import API_KEY, PATHS

# Innits the Key
openai.api_key = API_KEY

# Engines Model
MODEL = "gpt-3.5-turbo"

# Innit the logger
logger.remove()
logger.add(f"{PATHS['LOG_GENERATION_RESPONSES']}")

def GetResponce(problemNumber: int, prompt: str, temperature=0.6) -> str:
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
            "role": "user", "content": prompt},
            {"role": "user", "content": """You will be asked to answer programming questions in Python. You might 
                                            receive some code to include. When asked, all you should return 
                                            is only the python code. No comments, no explanation. The method after the 
                                            TODO comment should be able to immediately run once returned."""}
        ],
        temperature=temperature,
    )
    genResponse = response['choices'][0]['message']['content']
    logger.info(f"GENERATED RESPONSE FOR PROBLEM {problemNumber}: ''' {genResponse} '''\n\n")
    return genResponse