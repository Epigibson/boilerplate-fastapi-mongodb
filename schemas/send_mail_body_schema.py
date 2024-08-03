from pydantic import BaseModel


class SendEmail(BaseModel):
    email: str
    subject: str
    body: str
