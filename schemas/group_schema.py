from datetime import datetime
from typing import Optional
from uuid import UUID

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str
    description: str
    couch: Optional[str]
    members: Optional[list[PydanticObjectId]] = []
    admin: Optional[str]
    status: str
    capacity: int
    schedule: list[str]
    schedule_initial_final: list[str]


class GroupOut(BaseModel):
    _id: PydanticObjectId = Field(alias="_id")
    id: UUID
    name: str
    description: str
    couch: str
    members: list[PydanticObjectId]
    admin: str
    status: str
    capacity: int
    schedule: list[str]
    schedule_initial_final: list[str]


class GroupUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    couch: Optional[str]
    members: Optional[list[PydanticObjectId]]
    admin: Optional[str]
    status: Optional[str]
    capacity: Optional[int]
    schedule: Optional[list[str]]
    schedule_initial_final:  Optional[list[str]]
    updated_at: datetime = Field(default_factory=datetime.now)
