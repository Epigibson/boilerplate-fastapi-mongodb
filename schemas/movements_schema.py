from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from core.adjust_datetime import get_current_time_adjust
from models.choices.action_types import ActionTypes
from models.choices.modeules_choices import ModuleTypes
from models.choices.movemen_type import MovementType


class MovementCreate(BaseModel):
    type: MovementType
    action: ActionTypes
    module: ModuleTypes
    responsible_id: PydanticObjectId
    responsible_name: str
    created_at: Optional[datetime] = get_current_time_adjust()
    updated_at: Optional[datetime] = get_current_time_adjust()
    