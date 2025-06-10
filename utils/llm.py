import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_openAI(instructions: str, input: str | dict | list, model: str = "gpt-4.1-nano") -> str:
    """
    Call OpenAI's chat completion API using a system instruction and user input.
    """
    if not isinstance(input, str):
        input = json.dumps(input)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": input}
        ]
    )
    return response.choices[0].message.content.strip()
