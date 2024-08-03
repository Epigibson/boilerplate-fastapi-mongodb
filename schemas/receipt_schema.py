from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from models.choices.receipt_types import ReceiptType


class ReceiptCreate(BaseModel):
    receipt_type: ReceiptType
    receipt_amount: float
    receipt_amount_balance: float
    receipt_description: str
    receipt_status: str
    comment: Optional[str] = None
    user_id: PydanticObjectId
