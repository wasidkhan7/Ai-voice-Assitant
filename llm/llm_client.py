# Take user text → Send it to the LLM → Return the AI response.

"""
LLM service for generating AI responses using OpenAI.
"""

from typing import Any
import logging

from openai import OpenAI

from config.settings import LLM_MODEL, OPENAI_API_KEY
from utils.helpers import clean_text
from utils.prompts import SYSTEM_PROMPT
from typing import Any

Message = dict[str, Any]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class LLMService:
    """
    Service responsible for communicating with the LLM.
    """

    def __init__(self) -> None:
        self.client = self._create_client()

    def _create_client(self) -> OpenAI:
        """
        Create and return the OpenAI client.
        """

        logging.info("Initializing OpenAI client...")

        client = OpenAI(api_key=OPENAI_API_KEY)

        logging.info("OpenAI client initialized successfully.")

        return client

    def generate_response(self,messages: list[Message],) -> str:
        """
        Generate a response from the LLM.

        Args:
            user_message:
                User input.

            system_prompt:
                System instruction.

        Returns:
            AI response.
        """

        logging.info("Generating response from GPT...")

        response = self.client.responses.create(
            model=LLM_MODEL,
            input=messages,)

        text = clean_text(response.output_text)

        logging.info("Response generated successfully.")

        return text


if __name__ == "__main__":

    llm = LLMService()

    reply = llm.generate_response(
    [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "Introduce yourself in one sentence.",
        },
    ]
)

    print("\n========== GPT RESPONSE ==========\n")

    print(reply)

    print("\n==================================")