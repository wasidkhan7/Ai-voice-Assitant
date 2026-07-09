"""
Streamlit application for the AI Voice Assistant.
"""

import hashlib
import logging
from datetime import datetime

import streamlit as st

from config.settings import TEMP_AUDIO_DIR
from services.assistant import AssistantService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ AI Voice Assistant")

st.write(
    "Record a voice message and let the AI respond."
)

st.divider()


# -----------------------------
# Session State
# -----------------------------
if "assistant" not in st.session_state:
    st.session_state.assistant = AssistantService()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# -----------------------------
# Browser Microphone
# -----------------------------
audio_value = st.audio_input(
    "🎤 Record your message"
)


# -----------------------------
# Clear Conversation
# -----------------------------
if st.session_state.chat_history:

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history.clear()

        st.session_state.assistant.clear_conversation()

        # IMPORTANT:
        # Do NOT reset last_audio_hash to None here.
        # Otherwise, the old recording is treated as new.

        st.rerun()


# -----------------------------
# Process Recorded Audio
# -----------------------------
if audio_value is not None:

    audio_bytes = audio_value.getvalue()

    audio_hash = hashlib.sha256(
        audio_bytes
    ).hexdigest()

    if audio_hash != st.session_state.last_audio_hash:

        # Mark as processed before running the pipeline.
        st.session_state.last_audio_hash = audio_hash

        input_audio_path = (
            TEMP_AUDIO_DIR / "browser_recording.wav"
        )

        input_audio_path.write_bytes(audio_bytes)

        try:

            with st.spinner("🤖 Thinking..."):

                user_text, assistant_text, response_audio = (
                    st.session_state.assistant.chat_from_audio(
                        input_audio_path
                    )
                )

            response_audio_bytes = response_audio.read_bytes()

        except ValueError as error:

            st.warning(str(error))
            st.stop()

        except Exception as error:

            logging.exception(
                "Failed to process voice input: %s",
                error,
            )

            st.error(
                "Something went wrong while processing your voice. "
                "Please try again."
            )

            st.stop()

        # User message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_text,
                "timestamp": datetime.now(),
            }
        )

        # Assistant message
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": assistant_text,
                "timestamp": datetime.now(),
                "audio": response_audio_bytes,
            }
        )

        st.rerun()


# -----------------------------
# Conversation History
# -----------------------------
if st.session_state.chat_history:

    st.divider()
    st.subheader("Conversation")

    for index, message in enumerate(
        st.session_state.chat_history
    ):

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if (
                message["role"] == "assistant"
                and "audio" in message
            ):

                st.audio(
                    message["audio"],
                    format="audio/mp3",
                    autoplay=(
                        index
                        == len(st.session_state.chat_history) - 1
                    ),
                )

