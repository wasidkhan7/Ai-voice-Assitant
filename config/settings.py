# Purpose:

# Load environment variables
# API key
# Whisper model
# Audio settings
# Constants

"""
Application configuration settings.

Loads environment variables and exposes application-wide constants.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_AUDIO_DIR = BASE_DIR / "audio" / "temp"

# Create temp directory if it doesn't exist
TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# OpenAI Configuration
# ==========================================================

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

# ==========================================================
# Whisper Configuration
# ==========================================================

WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")

# ==========================================================
# Audio Configuration
# ==========================================================

SAMPLE_RATE: int = int(os.getenv("SAMPLE_RATE", 16000))

CHANNELS: int = int(os.getenv("CHANNELS", 1))

RECORD_DURATION: int = int(os.getenv("RECORD_DURATION", 5))

AUDIO_FILENAME: str = "recording.wav"

OUTPUT_FILENAME: str = "response.mp3"

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ==========================================================
# Text-to-Speech Configuration
# ==========================================================

TTS_MODEL: str = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")

TTS_VOICE: str = os.getenv("TTS_VOICE", "alloy")