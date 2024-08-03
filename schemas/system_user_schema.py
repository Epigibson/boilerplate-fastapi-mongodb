from typing import Optional
from beanie import Link
from pydantic import BaseModel, EmailStr, Field
from models.role_model import Role


class SystemUserCreate(BaseModel):
    email: EmailStr = Field(description="User's email.")
    name: Optional[str] = Field(description="Name.")
    password: str = Field(default="123456", min_length=4, max_length=25, description="User's password.")