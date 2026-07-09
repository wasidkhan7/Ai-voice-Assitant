# Convert AI-generated text into speech and save it as an MP3 file

"""
Text-to-Speech service using OpenAI.
"""

from pathlib import Path
from typing import Any
import logging

from openai import OpenAI

from config.settings import (
    OPENAI_API_KEY,
    TTS_MODEL,
    TTS_VOICE,
    TEMP_AUDIO_DIR,
    OUTPUT_FILENAME,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TextToSpeechService:
    """
    Service responsible for converting text into speech.
    """

    def __init__(self) -> None:
        self.client = self._create_client()
        self.output_path = TEMP_AUDIO_DIR / OUTPUT_FILENAME

    def _create_client(self) -> Any:
        """
        Create and return an OpenAI client.
        """

        logging.info("Initializing OpenAI client for TTS...")

        return OpenAI(api_key=OPENAI_API_KEY)

    def synthesize(self, text: str) -> Path:
        """
        Convert text into speech.

        Args:
            text:
                Input text.

        Returns:
            Path to the generated MP3 file.
        """

        logging.info("Generating speech...")

        response = self.client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
        )

        response.stream_to_file(self.output_path)

        logging.info("Speech generated successfully.")

        return self.output_path


if __name__ == "__main__":

    tts = TextToSpeechService()

    audio_path = tts.synthesize(
        "Hello Wasid! Congratulations on building your AI Voice Assistant."
    )

    print(audio_path)