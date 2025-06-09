from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DB_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
