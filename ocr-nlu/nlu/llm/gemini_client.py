"""Gemini adapter used only after deterministic NLU extraction and validation."""
import os
from google import genai

class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str = "gemini-3.5-flash-lite"):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("Set GEMINI_API_KEY before using GeminiClient")
        self.client = genai.Client(api_key=key)
        self.model = model

    def complete(self, prompt: str, *, json_mode: bool = True):
        config = {"response_mime_type": "application/json"} if json_mode else None
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        return response.text
