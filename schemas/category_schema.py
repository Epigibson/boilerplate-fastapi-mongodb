from datetime import datetime
from typing import Optional
from uuid import UUID
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field()
    description: str = Field()
    image: Optional[str] = Field()
    related_products: Optional[list[PydanticObjectId]] =[]


class CategoryOut(BaseModel):
    category_id: UUID
    name: str
    description: str
    image: Optional[str]
    related_products: Optional[list[PydanticObjectId]]
    status: bool
    created_at: datetime
    updated_at: datetime


class CategoryUpdate(BaseModel):
    description: Optional[str] = Field()
    image: Optional[str] = Field()
    related_products: Optional[list[PydanticObjectId]] = Field()
    status: Optional[bool] = Field()
    updated_at: datetime = Field(default_factory=datetime.now)
