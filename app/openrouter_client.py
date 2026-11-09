
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "google/gemma-4-26b-a4b-it:free"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing from .env")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "BENCHIN",
        }

        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0,
            "max_tokens": 500,
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=90,
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

