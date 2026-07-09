"""
Core assistant orchestration service.

Coordinates Speech-to-Text, conversation memory,
LLM response generation, and Text-to-Speech.
"""

import logging
from pathlib import Path

from stt.speech_to_text import SpeechToTextService
from llm.llm_client import LLMService
from tts.text_to_speech import TextToSpeechService
from services.memory import ConversationMemory


class AssistantService:
    """
    Core AI Voice Assistant service.

    This class is platform-independent. It does not record audio
    from a local microphone and does not play audio through local
    speakers.

    It accepts an existing audio file, processes it through the AI
    pipeline, and returns the generated results.
    """

    def __init__(self) -> None:
        logging.info("Initializing AI Voice Assistant...")

        self.stt = SpeechToTextService()
        self.llm = LLMService()
        self.tts = TextToSpeechService()
        self.memory = ConversationMemory()

        logging.info("Assistant initialized successfully.")

    def chat_from_audio(
        self,
        audio_path: Path,
    ) -> tuple[str, str, Path]:
        """
        Process an existing audio file through the complete
        AI Voice Assistant pipeline.

        Args:
            audio_path:
                Path to the user's recorded audio file.

        Returns:
            tuple[str, str, Path]:
                User transcription,
                assistant response,
                generated response audio path.
        """

        try:
            # -------------------------
            # Speech → Text
            # -------------------------
            user_text = self.stt.transcribe(audio_path)

            logging.info("User: %s", user_text)

            if not user_text.strip():
                raise ValueError(
                    "No speech could be detected in the audio."
                )

            # -------------------------
            # Add User Message to Memory
            # -------------------------
            self.memory.add_user_message(user_text)

            # -------------------------
            # Generate LLM Response
            # -------------------------
            assistant_response = self.llm.generate_response(
                self.memory.get_messages()
            )

            logging.info(
                "Assistant: %s",
                assistant_response,
            )

            # -------------------------
            # Add Assistant Response to Memory
            # -------------------------
            self.memory.add_assistant_message(
                assistant_response
            )

            # -------------------------
            # Text → Speech
            # -------------------------
            response_audio = self.tts.synthesize(
                assistant_response
            )

            return (
                user_text,
                assistant_response,
                response_audio,
            )

        except Exception as error:
            logging.exception(
                "Assistant pipeline failed: %s",
                error,
            )
            raise

    def clear_conversation(self) -> None:
        """
        Reset the assistant's conversation memory.
        """

        self.memory.reset()

        logging.info("Conversation memory cleared.")