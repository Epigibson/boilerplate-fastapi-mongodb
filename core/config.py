from typing import Set
from pydantic import BaseSettings
from decouple import config
from pytz import timezone


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 999
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    ALLOWED_METHODS: Set[str] = {"*"}
    ALLOWED_HEADERS: Set[str] = {"*"}
    ALLOWED_CREDENTIALS: bool = True

    PROJECT_NAME: str = "Sports Manager"

    SENDGRID_API_KEY = config("SENDGRID_API_KEY")
    ACCOUNT_SID = config("ACCOUNT_SID")
    AUTH_TOKEN = config("AUTH_TOKEN")

    TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = config("TWILIO_NUMBER")

    CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET")

    MONGO_CONNECTION_STRING = config("MONGO_CONNECTION_STRING", cast=str)

    MERCADO_PAGO_PUBLIC_KEY = config("MERCADO_PAGO_PUBLIC_KEY")
    MERCADO_PAGO_ACCESS_TOKEN = config("MERCADO_PAGO_ACCESS_TOKEN")

    # Define la zona horaria desde una variable de entorno
    TIMEZONE: str = config("TIMEZONE")
    local_tz = timezone(TIMEZONE)

    class Config:
        case_sensitive = True


settings = Settings()
