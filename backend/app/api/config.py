from pydantic import BaseSettings


class Settings(BaseSettings):
    DEFAULT_VAR="some default string value" # default value if env variable does not exist
    SECRET_KEY: str
    APP_MAX: int = 100
    FIRST_USER_MAIL: str
    FIRST_USER_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE_URL: str


    class Config:
        env_file: str  = ".env" # default .env file

