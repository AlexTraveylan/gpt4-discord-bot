from dataclasses import dataclass, field
from typing import Literal

from app.core.constants import BOT_INSTRUCTIONS, BOT_NAME, EXAMPLE_CONVOS

ROLE = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Pmessage:
    role: ROLE
    content: str

    def render(self) -> dict[str, str]:
        return self.__dict__


@dataclass()
class Conversation:
    messages: list[Pmessage] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        """
        Initialize a new conversation with the bot. set the initial prompt.
        """
        name_message = Pmessage("system", f"Ton nom est {BOT_NAME}")
        presentation_message = Pmessage("system", BOT_INSTRUCTIONS)
        intro_convo = Pmessage(
            "system", "Voici des exemples de conversations avec moi :"
        )
        exemples_convo = [Pmessage("system", convo) for convo in EXAMPLE_CONVOS]

        self.messages = [
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
        self.messages.append(message)

    def render(self) -> list[dict[str, str]]:
        """render the conversation into a list of dict

        Returns
        -------
        list[dict[str, str]]
            a list of dict representing the conversation
        """
        return [message.render() for message in self.messages]


class ConversionState:
    def __init__(self):
        self.conversation = Conversation()
        self.is_on = False

    def reset(self):
        self.conversation = Conversation()
        self.is_on = True
