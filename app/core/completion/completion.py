from attr import dataclass
from app.core.completion.base import ConversionState, Pmessage
import openai

from app.core.constants import MODEL
from app.core.logger.logger import LOGGER


@dataclass
class CompletionData:
    reply_text: str | None
    total_tokens: str | None

    @classmethod
    def from_dict(cls, data: dict) -> None:
        reply_text = data["choices"][0]["message"]["content"].strip()
        total_tokens = data["usage"]["total_tokens"]

        return CompletionData(reply_text, total_tokens)

    def render(self) -> dict[str, str]:
        return Pmessage("assistant", self.reply_text).render()


def generate_completion_response(state: ConversionState) -> CompletionData:
    try:
        prompt = state.conversation.render()
        response = openai.ChatCompletion.create(
            model=MODEL, messages=prompt, temperature=1, top_p=0.9, max_tokens=2048
        )

        return CompletionData.from_dict(response)
    except Exception as e:
        LOGGER.error(str(e))
