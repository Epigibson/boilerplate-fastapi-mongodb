from datetime import datetime
from typing import Optional
from uuid import UUID
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, Field

from models.permission_model import Permission


class RoleCreate(BaseModel):
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)
    permissions: Optional[list[Link[Permission]]] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Admin",
                "description": "This is an Admin role",
                "permissions": ['65d662f3751e027f07175ae0', '65d662fd751e027f07175ae1', '65d66305751e027f07175ae2'],
            }
        }
        arbitrary_types_allowed = True
        json_encoders = {
            UUID: str,
        }
        allow_population_by_field_name = True
        validate_assignment = True
        extra = "forbid"
        exclude_unset = True
        underscore_attrs_are_private = True
        keep_untouched = (Link,)
        use_enum_values = True


class RolOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    role_id: UUID
    name: str
    description: str
    permissions: list[Link[Permission]]
    created_at: datetime
    updated_at: datetime


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(max_length=255)
    description: Optional[str] = Field(max_length=255)
    permissions: Optional[list[Link[Permission]]] = Field()
