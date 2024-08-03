from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, PydanticObjectId
from pydantic import Field

from core.adjust_datetime import get_current_time_adjust
from models.choices.action_types import ActionTypes
from models.choices.modeules_choices import ModuleTypes
from models.choices.movemen_type import MovementType


class Movement(Document):
    movement_id: UUID = Field(default_factory=uuid4, unique=True)
    type: MovementType
    action: ActionTypes
    module: ModuleTypes
    responsible_id: PydanticObjectId
    responsible_name: str
    is_deleted: bool = False
    is_archived: bool = False
    model_affected: str = Field(default="")
    model_field_id: PydanticObjectId = Field(default=None)
    model_field_helper: str = Field(default="")
    created_at: datetime = get_current_time_adjust()
    updated_at: datetime = get_current_time_adjust()
