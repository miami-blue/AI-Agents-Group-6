import os
from dotenv import load_dotenv
from google import genai


# Load environment variables from .env file
load_dotenv()

# Config Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=api_key)

def get_llm_response(prompt: str, model: str = "gemini-2.0-flash") -> str:
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to generate LLM response: {str(e)}")