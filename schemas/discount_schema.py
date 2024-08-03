from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class DiscountCreate(BaseModel):
    product_id: Optional[PydanticObjectId]
    discount_name: str
    discount_description: str
    discount_percentage: float
    discount_amount: Optional[float]
    discount_code: str
    is_active: Optional[bool]
    is_recurrent: Optional[bool]
    users: Optional[list[PydanticObjectId]]
    athletes: Optional[list[PydanticObjectId]]


class DiscountUpdate(BaseModel):
    product_id: Optional[PydanticObjectId]
    discount_name: Optional[str]
    discount_description: Optional[str]
    discount_percentage: Optional[float]
    discount_amount: Optional[float]
    discount_code: Optional[str]
    is_recurrent: Optional[bool]
    is_active: Optional[bool]
    users: Optional[list[PydanticObjectId]]
    athletes: Optional[list[PydanticObjectId]]
