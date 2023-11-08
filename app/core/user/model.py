"""User model for the app"""
from dataclasses import dataclass
from typing import Literal

PurchaseType = Literal["free", "key_owner", "premium", "developer"]


@dataclass
class UserApp:
    """A user of the app"""

    discord_id: str
    email: str
    purchase: PurchaseType = "free"
    usage: float
