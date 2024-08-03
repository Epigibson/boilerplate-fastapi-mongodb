from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class HistoryPaymentCreate(BaseModel):
    receipt_id: Optional[PydanticObjectId]
    user: PydanticObjectId
    receipt_type: Optional[str]
    concept: Optional[str]
    user_name: Optional[str]
    athlete:  PydanticObjectId
    athlete_name: Optional[str]
    amount: float
    status: Optional[str]
    payment_type: Optional[str]
    payment_method: Optional[str]
    extension:  Optional[str]
    limit_date: Optional[datetime]
    package: Optional[PydanticObjectId]
    period_month: Optional[datetime]
    period_year: Optional[datetime]
