from typing import List
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    recipients: List[str]
    message: str


class NotificationOut(BaseModel):
    recipient: List[str]
    message: str
