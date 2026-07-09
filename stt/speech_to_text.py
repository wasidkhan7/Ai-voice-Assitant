#Convert:recording.wav  into"Hello ChatGPT, how are you?"speech-to-text using OpenAI Whisper running locally on your RTX 3060.

#using OpenAI Whisper running locally on your RTX 3060.
"""
Speech-to-Text service using OpenAI Whisper.
"""

from pathlib import Path
import logging

import torch
import whisper

from config.settings import WHISPER_MODEL
from utils.helpers import clean_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SpeechToTextService:
    """
    Service responsible for converting speech into text.
    """

    def __init__(self) -> None:
        """
        Initialize the Speech-to-Text service.
        """

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self._load_model()

    def _load_model(self):
        """
        Load the Whisper model onto the appropriate device.

        Returns:
            Whisper model instance.
        """

        logging.info(
            f"Loading Whisper model '{WHISPER_MODEL}' on {self.device.upper()}..."
        )

        model = whisper.load_model(
            WHISPER_MODEL,
            device=self.device,
        )

        logging.info("Whisper model loaded successfully.")

        return model

    def transcribe(self, audio_path: Path) -> str:
        """
        Convert speech to text.

        Args:
            audio_path:
                Path to the audio file.

        Returns:
            Transcribed text.
        """

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        logging.info("Transcribing audio...")

        result = self.model.transcribe(str(audio_path))

        text = clean_text(result["text"])

        logging.info("Transcription completed.")

        return text


if __name__ == "__main__":

    from config.settings import TEMP_AUDIO_DIR

    stt = SpeechToTextService()

    text = stt.transcribe(
        TEMP_AUDIO_DIR / "recording.wav"
    )

    print("\n========== TRANSCRIPTION ==========")
    print(text)
    print("===================================")