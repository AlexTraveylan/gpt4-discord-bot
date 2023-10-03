import openai

from app.core.create_image.base import URL, ResponseImage, Size
from app.core.logger.logger import LOGGER


def create_image(prompt: str, nb_images_requested: int, size: Size) -> list[URL]:
    try:
        response: ResponseImage = openai.Image.create(prompt=prompt, n=nb_images_requested, size=size.value)
        return [image["url"] for image in response["data"]]
    except Exception as e:
        LOGGER.error(str(e))
        return []
