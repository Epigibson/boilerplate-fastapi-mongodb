from pydantic import BaseModel, validator


class PaymentInfo:
    id: str


class PaymentData(BaseModel):
    action: str
    api_version: str
    data: dict
    date_created: str
    id: str
    live_mode: bool
    type: str
    user_id: int
