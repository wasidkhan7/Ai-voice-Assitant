"""
Conversation memory service.
"""

from utils.prompts import SYSTEM_PROMPT


class ConversationMemory:
    """
    Stores conversation history for the assistant.
    """

    def __init__(self) -> None:

        self.reset()

    def reset(self) -> None:
        """
        Reset the conversation history.
        """

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def add_user_message(self, message: str) -> None:

        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:

        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_messages(self) -> list[dict]:
        """
        Return the conversation history.
        """

        return self.messages