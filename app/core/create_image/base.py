from enum import StrEnum
from typing import Literal, TypedDict


class Size(StrEnum):
    SMALL = "256x256"
    MEDIUM = "512x512"
    LARGE = "1024x1024"


def factory_size(size: int) -> Size:
    if size == 0:
        return Size.SMALL
    elif size == 1:
        return Size.MEDIUM
    elif size == 2:
        return Size.LARGE
    else:
        return Size.MEDIUM


URL = str


class ResponseImage(TypedDict):
    created: int
    data: list[dict[Literal["url"], URL]]
