from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class PermissionCreate(BaseModel):
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)


class PermissionOut(BaseModel):
    permission_id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(max_length=255)
    description: Optional[str] = Field(max_length=255)
