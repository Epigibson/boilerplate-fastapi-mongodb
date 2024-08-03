from typing import Optional
from uuid import UUID
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field

from models.role_model import Role


class UserAuth(BaseModel):
    email: EmailStr = Field(description="User's email.")
    tutors_name_one: Optional[str] = Field(description="One Tutors name.")
    tutors_name_two: Optional[str] = Field(description="Two Tutors name.")
    password: str = Field(default="123456", min_length=4, max_length=25, description="User's password.")
    name: str = Field(min_length=3, max_length=50, description="User's name.")
    gender: str = Field(description="User's gender.")
    age: Optional[int] = Field(description="User's age.")
    sport_preference: Optional[str] = Field(description="User's sport preference.")
    hobbies: Optional[list[str]] = Field(description="User's hobbies")
    phone: Optional[int] = Field(description="User's phone number.")
    mobile: Optional[int] = Field(description="User's mobile number.")
    birthday: Optional[str] = Field(description="User's birthday.")
    street_name: Optional[str] = Field(description="User's street name.")
    street_number: Optional[str] = Field(description="User's street number.")
    zip_code: Optional[int] = Field(description="User's zip code.")
    role: Optional[Link[Role]]
    user_type: Optional[str]
    groups: Optional[list[PydanticObjectId]]


class UserInscription(BaseModel):
    email: EmailStr
    tutors_name: Optional[str]
    username: Optional[str]
    name: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    sport_preference: Optional[str]
    hobbies: Optional[list[str]]
    phone: Optional[int]


class UserOut(BaseModel):
    user_id: UUID
    hashed_password: str
    email: EmailStr
    name: str
    tutors_name_one: str
    tutors_name_two: str
    tuition: Optional[str]
    phone: Optional[int]
    mobile: Optional[int]
    gender: str
    age: int
    username: str
    role: Optional[Link[Role]]
    status: Optional[bool]
    avatar: Optional[str]
    user_type: str
    groups: Optional[list[PydanticObjectId]]
    is_inscribed: bool
    user_count: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(description="User's email.")
    name: Optional[str] = Field(description="User's name.")
    tutors_name_one: Optional[str] = Field(description="One Tutors name.")
    tutors_name_two: Optional[str] = Field(description="Two Tutors name.")
    role: Optional[Link[Role]]
    gender: Optional[str]
    phone: Optional[int]
    mobile: Optional[int]
    birthday: Optional[str]
    address: Optional[str]
    status: Optional[bool]
    avatar: Optional[str]
    age: Optional[int]
    groups: Optional[list[PydanticObjectId]]
