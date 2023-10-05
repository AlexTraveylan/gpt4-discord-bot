from dataclasses import dataclass
from typing import Literal

PurchaseType = Literal["free", "key_owner", "premium", "developer"]


@dataclass
class User_app:
    discord_id: str
    email: str
    purchase: PurchaseType = "free"
    usage: float
