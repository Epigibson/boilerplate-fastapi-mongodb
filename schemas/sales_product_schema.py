from typing import Optional

from pydantic import BaseModel, Field


class SalesProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity_stock: Optional[int] = Field(default=1)


class SalesProductUpdate(BaseModel):
    name: Optional[str]
    escription: Optional[str]
    price: Optional[float]
    status: Optional[bool]
    quantity_stock: Optional[int]
