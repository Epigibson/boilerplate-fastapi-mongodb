from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from pydantic import Field, EmailStr

from core.adjust_datetime import get_current_time_adjust
from models.choices.user_types import Usertype
from models.role_model import Role


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Optional[str] = Field()
    name: Optional[str] = Field()
    gender:  Optional[str] = Field()
    age:  Optional[int] = Field()
    email: Indexed(EmailStr, unique=True)
    status: Optional[bool] = Field(default=True)
    hashed_password: Optional[str]
    phone: Optional[int] = Field(default=None)
    mobile: Optional[int] = Field(default=None)
    street_name: Optional[str] = Field()
    street_number: Optional[str] = Field()
    zip_code: Optional[int] = Field()
    avatar: Optional[str] = Field()
    user_type: Optional[Usertype] = Field(default=Usertype.user)
    positive_balance: Optional[float] = Field(default=0)

    role: Optional[Link[Role]] = Field()

    created_at: datetime = get_current_time_adjust()
    updated_at: datetime = get_current_time_adjust()

    class Settings:
        collection = "User"
