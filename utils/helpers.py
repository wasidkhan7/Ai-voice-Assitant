
# Cleaning user text
# Formatting AI responses
# Generating timestamps
# Validating API keys
# Checking file existence
# Creating filenames

# Instead of rewriting them in multiple files, we place them in helpers.py.
# This follows the DRY Principle (Don't Repeat Yourself).



#---------------------------------------------
# Let's start with only four helper functions that we'll actually use.
# --------------------------------------------

"""
Utility helper functions for the AI Voice Assistant.
"""

from datetime import datetime
from pathlib import Path

from config.settings import OPENAI_API_KEY, TEMP_AUDIO_DIR

# 1. Clean text : Removes unnecessary whitespace.
def clean_text(text: str) -> str:
    """
    Remove extra whitespace from text.

    Args:
        text: Input string.

    Returns:
        Cleaned string.
    """
    return " ".join(text.strip().split())

# 2. Timestamp: Useful for logging.
def get_timestamp() -> str:
    """
    Return the current timestamp.

    Returns:
        Current date and time as a string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 3. Check API key: Instead of crashing later:
def validate_api_key() -> bool:
    """
    Check whether the OpenAI API key is configured.

    Returns:
        True if the key exists, otherwise False.
    """
    return OPENAI_API_KEY is not None and OPENAI_API_KEY != ""

# 4. Generate audio path: Instead of hardcoding:
def get_audio_path(filename: str) -> Path:
    """
    Return the full path for an audio file.

    Args:
        filename: Name of the audio file.

    Returns:
        Full pathlib.Path object.
    """
    return TEMP_AUDIO_DIR / filename


# for testing purposes
if __name__ == "__main__":

    print(clean_text("   Hello      ChatGPT      "))
    print(get_timestamp())
    print(validate_api_key())
    print(get_audio_path("recording.wav"))