from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from beanie import Document, Link
from pydantic import Field

from core.adjust_datetime import get_current_time_adjust
from models.permission_model import Permission


class Role(Document):
    role_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str = Field()
    description: str = Field()
    permissions: Optional[list[Link[Permission]]] = Field([])
    created_at: datetime = get_current_time_adjust()
    updated_at: datetime = get_current_time_adjust()

    def commit(self):
        self.save()

    def __unicode__(self):
        return self.name
