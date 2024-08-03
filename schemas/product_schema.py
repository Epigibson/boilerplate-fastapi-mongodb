from datetime import datetime
from typing import Optional
from uuid import UUID
from beanie import Link
from pydantic import BaseModel, Field

from models.category_model import Category


class ProductCreate(BaseModel):
    product_name: str = Field()
    product_description: str = Field()
    brand: Optional[str] = Field()
    price: float = Field()
    payment_deadline: Optional[int] = Field()
    is_active: bool = Field(default=True)
    quantity_stock: Optional[int] = Field(default=1)
    images: Optional[list[str]] = Field()
    labels_tags: Optional[list[str]] = Field()
    category: Optional[str] = Field()
    is_temporary: Optional[bool] = Field(default=False)
    week_duration: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    business_policy: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_name": "Testing Product",
                "product_description": "Este es un producto de prueba",
                "brand": '65d662f3751e027f07175ae1',
                "price": 549.99,
                "payment_deadline": 8,
                "is_active": True,
                "quantity_stock": 1,
                "images": ['65d662f3751e027f07175ae0', '65d662fd751e027f07175ae1', '65d66305751e027f07175ae2'],
                "labels_tags": ['65d662f3751e027f07175ae0', '65d662fd751e027f07175ae1', '65d66305751e027f07175ae2'],
                "category": '65d662f3751e027f07175ae0'
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
        use_enum_values = True


class ProductOut(BaseModel):
    product_id: UUID
    product_name: str
    product_description: str
    brand: Optional[str]
    price: float
    payment_deadline: Optional[int]
    is_active: bool
    quantity_stock: Optional[int]
    images: Optional[list[str]]
    labels_tags: Optional[list[str]]
    category: str
    created_at: datetime
    updated_at: datetime


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field()
    product_description: Optional[str] = Field()
    brand: Optional[str] = Field()
    price: Optional[float] = Field()
    payment_deadline: Optional[int] = Field()
    is_active: Optional[bool] = Field()
    quantity_stock: Optional[int] = Field()
    images: Optional[list[str]] = Field()
    labels_tags: Optional[list[str]] = Field()
    category: Optional[str] = Field()
    updated_at: datetime = Field(default_factory=datetime.now)
    is_temporary: Optional[bool]
    week_duration: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    business_policy: Optional[bool]
