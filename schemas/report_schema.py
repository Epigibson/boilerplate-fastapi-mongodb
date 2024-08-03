from beanie import PydanticObjectId
from pydantic import BaseModel


class ListAthletesPayment(BaseModel):
    id: PydanticObjectId
    tuition: str
    name: str
    status: bool
    last_month_payments: list
    current_month_payments: list
    next_month_payments: list


class ListAthletesPaidOrNot(BaseModel):
    _id: PydanticObjectId
    user_id: PydanticObjectId
    user_name: str
    athlete_id: PydanticObjectId
    tuition: str
    name: str
    status: bool

    last_month_status: str
    last_month_amount_left: float
    last_month_amount_paid: float

    current_month_status: str
    current_month_amount_left: float
    current_month_amount_paid: float

    next_month_status: str
    next_month_amount_left: float
    next_month_amount_paid: float

