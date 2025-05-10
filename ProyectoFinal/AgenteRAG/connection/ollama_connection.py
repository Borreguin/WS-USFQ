import asyncio
import json

import httpx

# Ollama server URL
OLLAMA_URL = "http://localhost:11434/api/chat"
model_to_use = "codegemma"

async def get_completion(prompt: str, _model: str) -> str:
    """Calls the Ollama local server and returns the completion."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={"model": _model, "messages": [{"role": "user", "content": prompt}]}
            )
            response.raise_for_status()  # Raise an error for HTTP issues
            print("Response status code:", response)
            # Collect the streamed response
            full_content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        # covert the line string to json
                        json_data = json.loads(line)
                        message = json_data.get("message", "")
                        content = message.get("content", "")
                        full_content += content
                    except Exception as e:
                        print(f"Error processing chunk: {e}")

            return full_content

    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching the completion."

def main():
    """Main function to call the get_completion function."""
    prompt = "What is the capital of France?"
    completion = asyncio.run(get_completion(prompt, model_to_use))
    print(completion)

if __name__ == "__main__":
    main()