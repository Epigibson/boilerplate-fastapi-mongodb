from typing import Optional
from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field


class Configurations(Document):
    configuration_id: UUID = Field(default_factory=uuid4, unique=True)
    notifications: Optional[bool] = Field(default=True)
    email_notifications: Optional[list] = Field(default=[])
    generation_receipts:  Optional[str]

    def commit(self):
        self.save()

    class Config:
        orm_mode = True

    class Settings:
        collection = "Configurations"
