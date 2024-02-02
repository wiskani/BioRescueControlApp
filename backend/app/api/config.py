from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    DEFAULT_VAR: str = "some default string value"
    SECRET_KEY: str
    APP_MAX: int = 100
    FIRST_USER_MAIL: EmailStr
    FIRST_USER_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    DATABASE_URL_TEST: str
    NEXTJS_URL: str

    class Config:
        env_file: str = ".env"

