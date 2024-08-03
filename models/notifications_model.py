from typing import List
from beanie import Document


class Notifications(Document):
    recipient: List[str]
    message: str

    class Settings:
        collection = "Notifications"
