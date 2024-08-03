from typing import Optional
from pydantic import BaseModel, Field


class ConfigurationsCreate(BaseModel):
    email_notifications: Optional[list] = Field()
    notifications: Optional[bool] = Field(default=True)
    generation_receipts: Optional[str]


class ConfigurationsUpdate(BaseModel):
    notifications: Optional[bool]
    email_notifications: Optional[list]
    generation_receipts: Optional[str]

