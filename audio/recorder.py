# Record audio from the microphone and save it as a WAV file.

"""
Audio recording service for the AI Voice Assistant.
"""

from pathlib import Path
import logging

import sounddevice as sd
from scipy.io.wavfile import write

from config.settings import (
    SAMPLE_RATE,
    CHANNELS,
    RECORD_DURATION,
    AUDIO_FILENAME,
    TEMP_AUDIO_DIR,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class RecorderService:
    """
    Service responsible for recording microphone input.
    """

    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.output_path = TEMP_AUDIO_DIR / AUDIO_FILENAME

    def record(self, duration: int | None = None) -> Path:      
        """
        Record audio from the microphone.

        Args:
            duration (int):
                Recording duration in seconds.

        Returns:
            Path:
                Path to the recorded WAV file.
        """

        if duration is None:
            duration = RECORD_DURATION

        logging.info(f"Recording started for {duration} seconds...")

        print("\n🎤 Speak now...\n")

        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
        )

        sd.wait()

        write(
            str(self.output_path),
            self.sample_rate,
            recording,
        )

        logging.info("Recording saved successfully.")

        print(f"✅ Audio saved to:\n{self.output_path}\n")


        return self.output_path


if __name__ == "__main__":

    recorder = RecorderService()

    path = recorder.record(duration=5)

    print(f"Returned Path:\n{path}")