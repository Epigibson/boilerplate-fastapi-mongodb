from beanie import PydanticObjectId
from pydantic import BaseModel


class BalanceHistoryCreate(BaseModel):
    receipt_id: PydanticObjectId
    amount_balance_applied: float
    payment_method: str
