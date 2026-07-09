# Orchestrator

"""
Assistant orchestration service.

Coordinates all AI services together.
"""

from pathlib import Path
import logging

from audio.recorder import RecorderService
from audio.player import PlayerService
from stt.speech_to_text import SpeechToTextService
from llm.llm_client import LLMService
from tts.text_to_speech import TextToSpeechService
from services.memory import ConversationMemory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class AssistantService:
    """
    Main AI Voice Assistant.
    Responsible for orchestrating the complete pipeline.
    """

    def __init__(self) -> None:

        logging.info("Initializing AI Voice Assistant...")

        self.recorder = RecorderService()
        self.player = PlayerService()
        self.stt = SpeechToTextService()
        self.llm = LLMService()
        self.tts = TextToSpeechService()
        self.memory = ConversationMemory()

        logging.info("Assistant initialized successfully.")

        
    def chat(self) -> tuple[str, str]:
        """
        Execute one complete local voice conversation cycle.
        """

        audio_path = self.recorder.record()

        user_text, assistant_response, response_audio = (
            self.assistant.chat_from_audio(audio_path)
        )

        self.player.play(response_audio)

        return user_text, assistant_response

    def clear_conversation(self) -> None:
        """
        Clear the conversation memory.
        """
        self.memory.reset()

        logging.info("Conversation memory cleared.")

    def stop(self) -> None:
        """
        Stop the assistant playback.
        """
        self.player.stop()

        

if __name__ == "__main__":

    assistant = AssistantService()

    user_text, response = assistant.chat()

    print("\n==============================")
    print("USER")
    print("------------------------------")
    print(user_text)

    print("\nASSISTANT")
    print("------------------------------")
    print(response)
    print("==============================")

