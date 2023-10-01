from dataclasses import dataclass, field
import re
from typing import Literal

from interactions import TYPE_THREAD_CHANNEL

from app.core.constants import (
    BOT_INSTRUCTIONS,
    BOT_NAME,
    EXAMPLE_CONVOS,
    MAX_CHARS_PER_REPLY_MSG,
)

ROLE = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Pmessage:
    role: ROLE
    content: str

    def render(self) -> dict[str, str]:
        return self.__dict__


@dataclass()
class Conversation:
    init_prompt: list[Pmessage] = field(default_factory=list, init=False)
    messages: list[Pmessage] = field(default_factory=list, init=False)
    thread: TYPE_THREAD_CHANNEL = field(default=None, init=False)
    current_total_tokens: int = 0

    def __post_init__(self) -> None:
        """
        Initialize a new conversation with the bot. set the initial prompt.
        """
        name_message = Pmessage("system", f"Ton nom est {BOT_NAME}")
        presentation_message = Pmessage("system", BOT_INSTRUCTIONS)
        intro_convo = Pmessage("system", "Voici des exemples de conversations avec moi :")
        exemples_convo = [Pmessage("system", convo) for convo in EXAMPLE_CONVOS]

        self.init_prompt = [
            name_message,
            presentation_message,
            intro_convo,
            *exemples_convo,
        ]

    def add_message(self, message: Pmessage) -> None:
        """add a message to the conversation

        Parameters
        ----------
        message : Message
            the message to add to the conversation
        """
        if self.current_total_tokens > 1800:
            self.messages.pop(0)
            self.messages.pop(0)
        self.messages.append(message)

    def render(self) -> list[dict[str, str]]:
        """render the conversation into a list of dict

        Returns
        -------
        list[dict[str, str]]
            a list of dict representing the conversation
        """
        return [message.render() for message in [*self.init_prompt, *self.messages]]


class ConversionState:
    def __init__(self):
        self.conversation = Conversation()
        self.is_on = False

    def reset(self):
        self.conversation = Conversation()
        self.is_on = True

    def stop(self):
        self.is_on = False


@dataclass
class SplitTooLongMessage:
    message: str
    max_size: int = MAX_CHARS_PER_REPLY_MSG

    def result(self) -> list[str]:
        if len(self.message) <= self.max_size:
            return [self.message]

        parts = re.split(r"(```[^`]+```)", self.message)
        result = []
        for part in parts:
            if part.startswith("\n"):
                part = part.replace("\n", "", 1)
            if part.startswith("```"):
                result.extend(self._split_a_too_long_part_with_backticks(part))
            else:
                result.extend(self._split_a_too_long_part(part))

        return result

    def _split_with_backticks(self) -> list[str]:
        backtick_parts = re.split(r"(```[^`]+```)", self.message)
        backtick_parts = [part.strip() for part in backtick_parts if part]

        return backtick_parts

    def _split_a_too_long_part(self, part: str) -> list[str]:
        if len(part) <= self.max_size:
            return [part]

        lines = part.split("\n")
        part_1 = lines[: len(lines) // 2]
        part_2 = lines[len(lines) // 2 :]
        return ["\n".join(part_1), "\n".join(part_2)]

    def _split_a_too_long_part_with_backticks(self, part: str) -> list[str]:
        if len(part) <= self.max_size:
            return [part]

        words = part.split("\n")
        part_1 = words[: len(words) // 2]
        part_2 = words[len(words) // 2 :]

        return ["\n".join(part_1) + "\n```", "```" + "\n".join(part_2)]
