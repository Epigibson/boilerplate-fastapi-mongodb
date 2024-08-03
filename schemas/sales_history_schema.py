from datetime import datetime
from typing import Optional

import pytz
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class SalesHistoryCreate(BaseModel):
    product_id: PydanticObjectId
    product_name: str
    product_price: float
    product_quantity: int
    total_price: float
    payment_method: str
    is_lost: Optional[bool] = False


class SalesHistoryUpdate(BaseModel):
    product_id: Optional[PydanticObjectId]
    product_name: Optional[str]
    product_price: Optional[float]
    product_quantity: Optional[int]
    total_price: Optional[float]
    payment_method: Optional[str]
