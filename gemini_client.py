import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

client = genai.Client(api_key=API_KEY)


def generate_text(
    prompt: str,
    temperature: float = 0.3,
    max_output_tokens: int = 1200
) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens
            )
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"