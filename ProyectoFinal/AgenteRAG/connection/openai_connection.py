# import asyncio

# api_key = "sk-proj-"
# model = "gpt-3.5-turbo"

# from openai import AsyncOpenAI

# client = AsyncOpenAI(
#   api_key=api_key,
# )


# async def get_completion(prompt: str) -> str:
#     """Calls the AsyncOpenAI client and returns the completion."""
#     try:
#         response = await client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         print("API Response:", response)
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return "An error occurred while fetching the completion."


# def main():
#     """Main function to call the get_completion function."""
#     prompt = "What is the capital of France?"
#     completion = asyncio.run(get_completion(prompt))
#     print(completion)

# if __name__ == "__main__":
#     main()
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import pickle

from connection.ReadPDF import contenido, pdf1
from connection.keyandcontext import KeyAndContext

api_key = "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"
model = "gpt-3.5-turbo"

from openai import AsyncOpenAI

client = AsyncOpenAI(
  api_key=api_key,
)

async def get_completion(prompt: str) -> str:
    """Calls the AsyncOpenAI client and returns the completion."""
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        print("API Response:", response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching the completion."


def main():
    """Main function to call the get_completion function."""
    # prompt = "What is the capital of France?"
    # completion = asyncio.run(get_completion(prompt))
    # print(completion)
    prompt = "Dame las 20 palabras mas importantes del siguiente parrafo:"
    promptwithcontext = prompt + contenido[pdf1][0]
    key = asyncio.run(get_completion(promptwithcontext))

    print(key)
    nuevo_KeyAndContext = KeyAndContext()
    nuevo_KeyAndContext.key = key
    nuevo_KeyAndContext.content = contenido[pdf1][0]

    with open("nuevo.pkl", "wb") as archivo:
        pickle.dump(nuevo_KeyAndContext, archivo)

def readPickle(path):
    with open(path, "rb") as archivo:
        return pickle.load(archivo)

def sendQuestionFromUser(question):
    prompt = "Dame una lista de las 20 palabras mas importantes de esta pregunta"
    questionprompt = prompt + question
    key = asyncio.run(get_completion(questionprompt))
    return key

if __name__ == "__main__":
    # main()
    answer = readPickle("nuevo.pkl")
    print(answer)

    userQuestion = "Cual fue el incidente?"
    key = sendQuestionFromUser(userQuestion)
    print(key)

