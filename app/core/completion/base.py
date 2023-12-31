"""Base classes for completion."""
from dataclasses import dataclass, field
import re
from typing import Literal

from interactions import TYPE_THREAD_CHANNEL
from app.core.personnalities import Personality

from app.core.constants import MAX_CHARS_PER_REPLY_MSG, MAX_TOKENS, MAX_TOKENS_SECURITY

ROLE = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Pmessage:
    """A message in a conversation"""

    role: ROLE
    content: str

    def render(self) -> dict[str, str]:
        """render the message into a dict"""
        return self.__dict__


@dataclass()
class Conversation:
    """A conversation between a user and a bot"""

    bot: Personality = field(default=None, init=False)
    init_prompt: list[Pmessage] = field(default_factory=list, init=False)
    messages: list[Pmessage] = field(default_factory=list, init=False)
    thread: TYPE_THREAD_CHANNEL = field(default=None, init=False)
    current_total_tokens: int = 0

    def set_bot_personnality(self, bot: Personality) -> None:
        """
        Initialize a new conversation with the bot. set the initial prompt.
        """
        self.bot = bot
        self.init_prompt.append(Pmessage("system", f"Ton nom est {self.bot.name}"))
        if len(self.bot.instructions) > 0:
            self.init_prompt.append(Pmessage("system", self.bot.instructions))
        if len(self.bot.example_convos) > 0:
            self.init_prompt.append(
                Pmessage("system", "Voici des exemples de conversations entre toi et un user :")
            )
            self.init_prompt.extend(
                [Pmessage("system", convo) for convo in self.bot.example_convos]
            )

    def _remove_old_messages(self, message) -> None:
        """remove old messages from the conversation"""

        while self.current_total_tokens > MAX_TOKENS - MAX_TOKENS_SECURITY:
            token_removed = sum([len(message.content) for message in self.messages[:2]])
            self.messages.pop(0)
            self.messages.pop(0)
            self.current_total_tokens -= token_removed

    def add_message(self, message: Pmessage) -> None:
        """add a message to the conversation

        Parameters
        ----------
        message : Message
            the message to add to the conversation
        """
        self._remove_old_messages(message)
        self.messages.append(message)

    def render(self) -> list[dict[str, str]]:
        """render the conversation into a list of dict

        Returns
        -------
        list[dict[str, str]]
            a list of dict representing the conversation
        """
        return [message.render() for message in [*self.init_prompt, *self.messages]]

    def reset_messages(self) -> None:
        """reset the messages of the conversation"""
        self.messages = []


class ConversionState:
    """A state of a conversation"""

    def __init__(self):
        """initialize a new state of a conversation"""
        self.conversation = Conversation()
        self.is_on = False

    def reset(self):
        """reset the state of the conversation"""
        self.conversation = Conversation()
        self.is_on = True

    def stop(self):
        """stop the state of the conversation"""
        self.is_on = False


@dataclass
class SplitTooLongMessage:
    """Split a message if it is too long"""

    message: str
    max_size: int = MAX_CHARS_PER_REPLY_MSG

    def result(self) -> list[str]:
        """return the result of the split"""
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
        """split the message with backticks"""
        backtick_parts = re.split(r"(```[^`]+```)", self.message)
        backtick_parts = [part.strip() for part in backtick_parts if part]

        return backtick_parts

    def _split_a_too_long_part(self, part: str) -> list[str]:
        """split a part of the message if it is too long"""
        if len(part) <= self.max_size:
            return [part]

        lines = part.split("\n")
        part_1 = lines[: len(lines) // 2]
        part_2 = lines[len(lines) // 2 :]
        return ["\n".join(part_1), "\n".join(part_2)]

    def _split_a_too_long_part_with_backticks(self, part: str) -> list[str]:
        """split a part of the message if it is too long and contains backticks"""
        if len(part) <= self.max_size:
            return [part]

        langage = part.split("\n")[0].replace("```", "").replace("\n", "").strip()

        words = part.split("\n")
        part_1 = words[: len(words) // 2]
        part_2 = words[len(words) // 2 :]

        return ["\n".join(part_1) + "\n```", f"```{langage}" + "\n".join(part_2)]
