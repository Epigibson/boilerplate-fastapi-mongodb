from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class AthleteCreate(BaseModel):
    name: Optional[str]
    tuition:  Optional[str]
    gender: Optional[str]
    status: Optional[bool]
    birthday: Optional[str]
    age: Optional[int]
    sport_preference: Optional[str]
    hobbies: Optional[list[str]]
    street_name: Optional[str]
    street_number: Optional[str]
    zip_code: Optional[int]
    avatar: Optional[str]
    groups: Optional[list[PydanticObjectId]]
    is_inscribed: Optional[bool]
    products_which_inscribed: Optional[list[PydanticObjectId]]
    user_count: Optional[str]


class AthleteUpdate(BaseModel):
    name: Optional[str]
    email:  Optional[str]
    phone:  Optional[str]
    mobile:  Optional[str]
    tutors_name_one:   Optional[str]
    tutors_name_two:   Optional[str]
    tuition:  Optional[str]
    gender: Optional[str]
    status: Optional[bool]
    birthday: Optional[str]
    age: Optional[int]
    sport_preference: Optional[str]
    hobbies: Optional[list[str]]
    street_name: Optional[str]
    street_number: Optional[str]
    zip_code: Optional[int]
    avatar: Optional[str]
    groups: Optional[list[PydanticObjectId]]
    is_inscribed: Optional[bool]
    start_date: Optional[datetime]
    products_which_inscribed: Optional[list[PydanticObjectId]]
    user_count: Optional[str]