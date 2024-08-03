from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field

from core.adjust_datetime import get_current_time_adjust


class Permission(Document):
    permission_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str = Field()
    description: str = Field()
    created_at: datetime = get_current_time_adjust()
    updated_at: datetime = get_current_time_adjust()

    def __unicode__(self):
        return self.name
