"""Create an image from a prompt."""
from typing import Literal
from openai import OpenAI, OpenAIError
from app.core.constants import Parameters

from app.core.create_image.base import URL, Size
from app.core.logger.logger import LOGGER


def create_image(
    prompt: str, nb_images_requested: int, size: Size, style: Literal["vivid", "natural"]
) -> list[URL]:
    """Create an image from a prompt."""
    client = OpenAI(api_key=Parameters.OPENAI_API_KEY)

    try:
        response = client.images.generate(
            prompt=prompt,
            n=nb_images_requested,
            size=size.value,
            model="dall-e-3",
            quality="hd",
            style=style,
        )

        return [image.url for image in response.data]

    except OpenAIError as e:
        LOGGER.error(str(e))
        return [str(e)]
