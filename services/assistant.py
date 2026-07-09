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
        Execute one complete conversation.

        Returns:
            tuple[str, str]:
                (User transcription, AI response)
        """

        try:
            # -------------------------
            # Record Audio
            # -------------------------
            audio_path: Path = self.recorder.record()

            # -------------------------
            # Speech → Text
            # -------------------------
            user_text = self.stt.transcribe(audio_path)

            logging.info(f"User: {user_text}")

            # -------------------------
            # Store Conversation
            # -------------------------
            self.memory.add_user_message(user_text)

            # -------------------------
            # LLM Response
            # -------------------------
            assistant_response = self.llm.generate_response(
                self.memory.get_messages()
            )

            logging.info(
                f"Assistant: {assistant_response}"
            )

            #-------------------------
            # Store Conversation
            #-------------------------            
            self.memory.add_assistant_message(assistant_response
            )

            # -------------------------
            # Text → Speech
            # -------------------------
            response_audio = self.tts.synthesize(
                assistant_response
            )

            # -------------------------
            # Play Audio
            # -------------------------
            self.player.play(response_audio)

            return (
                user_text,
                assistant_response,
            )

        except Exception as error:

            logging.exception(
                f"Assistant pipeline failed: {error}"
            )

            return (
                "ERROR",
                "Sorry, something went wrong while processing your request.",
            )

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