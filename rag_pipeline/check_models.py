import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

print("\nModels supporting generateContent:\n")

for model in client.models.list():

    if "generateContent" in model.supported_actions:
        print(model.name)