
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()


class GnaniSTTClient:
    BASE_URL = "https://api.vachana.ai/stt/v3"
    MODEL = "prisma-v3.0"

    def __init__(self) -> None:
        self.api_key = os.getenv("GNANI_API_KEY_ID")

        if not self.api_key:
            raise ValueError("GNANI_API_KEY_ID is missing from .env")

    def transcribe(
        self,
        audio_path: str,
        language_code: str = "gu-IN,en-IN",
        output_format: str = "codemix",
    ) -> dict:
        audio_file = Path(audio_path)

        if not audio_file.is_file():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        headers = {
            "X-API-Key-ID": self.api_key,
        }

        data = {
            "model": self.MODEL,
            "language_code": language_code,
            "format": output_format,
        }

        with audio_file.open("rb") as audio:
            response = requests.post(
                self.BASE_URL,
                headers=headers,
                files={
                    "audio_file": (audio_file.name, audio)
                },
                data=data,
                timeout=60,
            )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            raise RuntimeError(
                f"Gnani transcription failed: {result}"
            )

        return result
