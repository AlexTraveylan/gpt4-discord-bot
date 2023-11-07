"""Base classes and types for creating images."""
from enum import Enum
from typing import Optional


class Size(Enum):
    """Size of the image."""

    SMALL = "256x256"
    MEDIUM = "512x512"
    LARGE = "1024x1024"
    HORIZONTAL = "1792x1024"
    VERTICAL = "1024x1792"


def factory_size(size: int) -> Size:
    """Factory to create a Size from an int."""

    if size == 0:
        return Size.SMALL

    if size == 1:
        return Size.MEDIUM

    if size == 2:
        return Size.LARGE

    if size == 3:
        return Size.HORIZONTAL

    if size == 4:
        return Size.VERTICAL

    return Size.MEDIUM


URL = Optional[str]
