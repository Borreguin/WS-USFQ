import asyncio

api_key = "sk-proj-"
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
    prompt = "What is the capital of France?"
    completion = asyncio.run(get_completion(prompt))
    print(completion)

if __name__ == "__main__":
    main()