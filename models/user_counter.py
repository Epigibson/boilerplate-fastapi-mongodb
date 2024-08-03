
from beanie import Document


class UserCounter(Document):
    counter: int = 1
