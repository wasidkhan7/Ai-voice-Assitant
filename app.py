"""
Streamlit application for the AI Voice Assistant.
"""

import logging

from datetime import datetime
import streamlit as st

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
    "Speak through your microphone and let the AI respond."
)

st.divider()


# -----------------------------
# Session State
# -----------------------------
if "assistant" not in st.session_state:
    st.session_state.assistant = AssistantService()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_listening" not in st.session_state:
    st.session_state.is_listening = False


# -----------------------------
# Buttons
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    start = st.button("🎤 Start Conversation")

with col2:
    stop = st.button("⏹️ Stop Conversation")

with col3:
    if st.session_state.chat_history:
        clear = st.button("🗑️ Clear Chat")
    else:
        clear = False


# -----------------------------
# Button Actions
# -----------------------------
if start:
    st.session_state.is_listening = True

if stop:
    st.session_state.is_listening = False
    st.session_state.assistant.stop()
    
# -----------------------------
# Start continuous Conversation
# -----------------------------
if st.session_state.is_listening:
        
    with st.spinner("🎤 Listening...please speak"):
        user_text, assistant_text = (
            st.session_state.assistant.chat()
        )

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_text,
                "timestamp": datetime.now(),
            }
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": assistant_text,
                "timestamp": datetime.now(),
            }
        )


#-----------
# stop
#---------
if stop:
    st.session_state.is_listening = False


# -----------------------------
# Clear Conversation
# -----------------------------
if clear:

    st.session_state.chat_history.clear()

    st.session_state.assistant.clear_conversation()

    st.rerun()

# -----------------------------
# Results
# -----------------------------
if st.session_state.chat_history:

    st.divider()

    st.subheader("Conversation")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])
